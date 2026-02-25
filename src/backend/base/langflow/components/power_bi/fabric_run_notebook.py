import json
import time

import httpx

from langflow.custom import Component
from langflow.io import BoolInput, IntInput, Output, SecretStrInput, StrInput
from langflow.schema import Data

_FABRIC_SCOPE = "https://api.fabric.microsoft.com/.default"
_FABRIC_API_BASE = "https://api.fabric.microsoft.com/v1"
_TOKEN_URL_TEMPLATE = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

_POLL_INTERVAL_SECONDS = 10
_MAX_POLL_SECONDS = 300


class FabricRunNotebookComponent(Component):
    """Run a Microsoft Fabric notebook and optionally wait for it to finish.

    Submits a *RunNotebook* job via the Fabric REST API and returns a
    :class:`~langflow.schema.Data` item with the job instance ID and final
    status.  When *Wait for Completion* is enabled the component polls the job
    status until the notebook succeeds, fails, or the *Timeout* is exceeded.
    """

    display_name = "Fabric Run Notebook"
    description = (
        "Trigger a Microsoft Fabric notebook run and optionally wait for completion. "
        "Returns job status and metadata."
    )
    documentation = (
        "https://learn.microsoft.com/rest/api/fabric/notebook/items/run-on-demand-notebook"
    )
    trace_type = "tool"
    icon = "Microsoft"
    name = "FabricRunNotebook"

    inputs = [
        StrInput(
            name="tenant_id",
            display_name="Tenant ID",
            required=True,
            info="Azure Active Directory tenant (directory) ID.",
        ),
        StrInput(
            name="client_id",
            display_name="Client ID",
            required=True,
            info="Azure AD application (client) ID with Fabric API permissions.",
        ),
        SecretStrInput(
            name="client_secret",
            display_name="Client Secret",
            required=True,
            info="Azure AD application client secret.",
        ),
        StrInput(
            name="workspace_id",
            display_name="Workspace ID",
            required=True,
            info="Microsoft Fabric workspace ID that contains the notebook.",
        ),
        StrInput(
            name="notebook_id",
            display_name="Notebook ID",
            required=True,
            info="The unique ID of the Fabric notebook item to run.",
        ),
        StrInput(
            name="notebook_parameters",
            display_name="Notebook Parameters (JSON)",
            required=False,
            value="",
            info=(
                "Optional JSON string of parameters to pass to the notebook. "
                'Example: {"param_name": {"value": "hello", "type": "string"}}'
            ),
        ),
        BoolInput(
            name="wait_for_completion",
            display_name="Wait for Completion",
            value=True,
            info=(
                "When enabled, the component polls until the notebook job finishes "
                "or the timeout is reached."
            ),
        ),
        IntInput(
            name="timeout_seconds",
            display_name="Timeout (seconds)",
            value=_MAX_POLL_SECONDS,
            advanced=True,
            info="Maximum seconds to wait when 'Wait for Completion' is enabled.",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Job Status", method="run_notebook"),
    ]

    # ------------------------------------------------------------------
    # Public method
    # ------------------------------------------------------------------

    def run_notebook(self) -> Data:
        try:
            with httpx.Client(timeout=30) as client:
                token = self._get_access_token(client)
                job_id, location = self._submit_notebook_run(client, token=token)

                if not self.wait_for_completion:
                    result = Data(
                        text=f"Notebook job submitted: {job_id}",
                        data={
                            "source": "fabric",
                            "job_instance_id": job_id,
                            "workspace_id": self.workspace_id,
                            "notebook_id": self.notebook_id,
                            "status": "submitted",
                        },
                    )
                    self.status = result
                    return result

                final_status = self._poll_until_done(client, token=token, location=location)
                result = Data(
                    text=f"Notebook job {job_id} finished with status: {final_status}",
                    data={
                        "source": "fabric",
                        "job_instance_id": job_id,
                        "workspace_id": self.workspace_id,
                        "notebook_id": self.notebook_id,
                        "status": final_status,
                    },
                )
                self.status = result
                return result
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Microsoft Fabric notebook run failed."
            raise ValueError(msg) from exc

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def _get_access_token(self, client: httpx.Client) -> str:
        url = _TOKEN_URL_TEMPLATE.format(tenant_id=self.tenant_id)
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": _FABRIC_SCOPE,
        }
        try:
            resp = client.post(url, data=payload)
            resp.raise_for_status()
            token = resp.json().get("access_token")
            if not token:
                msg = "Unable to obtain Fabric access token."
                raise ValueError(msg)
            return token
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Fabric authentication failed. Verify tenant ID, client ID and client secret."
            raise ValueError(msg) from exc

    # ------------------------------------------------------------------
    # Notebook run
    # ------------------------------------------------------------------

    def _submit_notebook_run(self, client: httpx.Client, *, token: str) -> tuple[str, str]:
        endpoint = (
            f"{_FABRIC_API_BASE}/workspaces/{self.workspace_id}"
            f"/items/{self.notebook_id}/jobs/instances?jobType=RunNotebook"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        body: dict = {}
        if self.notebook_parameters and self.notebook_parameters.strip():
            try:
                params = json.loads(self.notebook_parameters)
                body["executionData"] = {"parameters": params}
            except json.JSONDecodeError as exc:
                msg = "Notebook Parameters must be valid JSON."
                raise ValueError(msg) from exc

        try:
            resp = client.post(endpoint, headers=headers, json=body)
            resp.raise_for_status()
            location = resp.headers.get("Location", "")
            # Extract job instance ID from Location header or response body
            job_id = self._extract_job_id(resp, location)
            return job_id, location
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Failed to submit Fabric notebook job."
            raise ValueError(msg) from exc

    def _extract_job_id(self, resp: httpx.Response, location: str) -> str:
        try:
            data = resp.json()
            if isinstance(data, dict):
                return data.get("id", location.split("/")[-1] if location else "unknown")
        except Exception:  # noqa: BLE001
            pass
        return location.split("/")[-1] if location else "unknown"

    def _poll_until_done(self, client: httpx.Client, *, token: str, location: str) -> str:
        if not location:
            return "submitted"

        headers = {"Authorization": f"Bearer {token}"}
        timeout = max(10, int(self.timeout_seconds or _MAX_POLL_SECONDS))
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            try:
                resp = client.get(location, headers=headers)
                resp.raise_for_status()
                status = resp.json().get("status", "Unknown")
                if status in {"Completed", "Cancelled", "Failed", "Deduped"}:
                    return status
            except httpx.HTTPError:
                pass
            time.sleep(_POLL_INTERVAL_SECONDS)

        return "Timeout"
