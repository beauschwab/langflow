import httpx

from langflow.custom import Component
from langflow.io import DropdownInput, Output, SecretStrInput, StrInput
from langflow.schema import Data

_POWERBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"
_POWERBI_API_BASE = "https://api.powerbi.com/v1.0/myorg"
_TOKEN_URL_TEMPLATE = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"


class PowerBIRefreshDatasetComponent(Component):
    """Trigger an on-demand refresh of a Power BI dataset (semantic model).

    The component submits a refresh request and returns a :class:`~langflow.schema.Data`
    item with the HTTP status code and any message returned by the API.  For
    capacity-based workspaces the refresh is asynchronous — poll the refresh
    history endpoint separately to confirm completion.
    """

    display_name = "Power BI Refresh Dataset"
    description = (
        "Trigger an on-demand data refresh for a Power BI dataset (semantic model) "
        "in a specified workspace."
    )
    documentation = (
        "https://learn.microsoft.com/rest/api/power-bi/datasets/refresh-dataset-in-group"
    )
    trace_type = "tool"
    icon = "PowerBI"
    name = "PowerBIRefreshDataset"

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
            info="Azure AD application (client) ID with Power BI API permissions.",
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
            info="Power BI workspace (group) ID that contains the dataset.",
        ),
        StrInput(
            name="dataset_id",
            display_name="Dataset / Semantic Model ID",
            required=True,
            info="The unique ID of the Power BI dataset or semantic model to refresh.",
        ),
        DropdownInput(
            name="notify_option",
            display_name="Notify Option",
            options=["NoNotification", "MailOnCompletion", "MailOnFailure"],
            value="NoNotification",
            advanced=True,
            info="Email notification behavior when the refresh completes.",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Refresh Status", method="refresh_dataset"),
    ]

    # ------------------------------------------------------------------
    # Public method
    # ------------------------------------------------------------------

    def refresh_dataset(self) -> Data:
        try:
            with httpx.Client(timeout=30) as client:
                token = self._get_access_token(client)
                result = self._trigger_refresh(client, token=token)
                self.status = result
                return result
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Power BI dataset refresh failed."
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
            "scope": _POWERBI_SCOPE,
        }
        try:
            resp = client.post(url, data=payload)
            resp.raise_for_status()
            token = resp.json().get("access_token")
            if not token:
                msg = "Unable to obtain Power BI access token."
                raise ValueError(msg)
            return token
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Power BI authentication failed. Verify tenant ID, client ID and client secret."
            raise ValueError(msg) from exc

    # ------------------------------------------------------------------
    # Refresh trigger
    # ------------------------------------------------------------------

    def _trigger_refresh(self, client: httpx.Client, *, token: str) -> Data:
        endpoint = (
            f"{_POWERBI_API_BASE}/groups/{self.workspace_id}"
            f"/datasets/{self.dataset_id}/refreshes"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        body = {"notifyOption": self.notify_option}
        try:
            resp = client.post(endpoint, headers=headers, json=body)
            resp.raise_for_status()
            return Data(
                text=f"Refresh triggered for dataset {self.dataset_id}",
                data={
                    "source": "power_bi",
                    "dataset_id": self.dataset_id,
                    "workspace_id": self.workspace_id,
                    "http_status": resp.status_code,
                    "message": "Refresh request accepted." if resp.status_code == 202 else resp.text,
                },
            )
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Power BI refresh request failed. Check dataset ID and workspace ID."
            raise ValueError(msg) from exc
