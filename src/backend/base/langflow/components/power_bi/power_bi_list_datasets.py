import httpx

from langflow.custom import Component
from langflow.io import Output, SecretStrInput, StrInput
from langflow.schema import Data

_POWERBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"
_POWERBI_API_BASE = "https://api.powerbi.com/v1.0/myorg"
_TOKEN_URL_TEMPLATE = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"


class PowerBIListDatasetsComponent(Component):
    """List Power BI datasets (semantic models) in a workspace.

    Returns one :class:`~langflow.schema.Data` item per dataset containing its
    ID, name, configured-by, web URL, and refresh schedule information.  Use the
    dataset ID from this output as the *Dataset / Semantic Model ID* input for
    :class:`PowerBIDAXQueryComponent` or :class:`PowerBIRefreshDatasetComponent`.
    """

    display_name = "Power BI List Datasets"
    description = (
        "List all datasets (semantic models) in a Power BI workspace and return their "
        "IDs, names, and metadata."
    )
    documentation = "https://learn.microsoft.com/rest/api/power-bi/datasets/get-datasets-in-group"
    trace_type = "tool"
    icon = "PowerBI"
    name = "PowerBIListDatasets"

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
            info="Power BI workspace (group) ID to list datasets from.",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Datasets", method="list_datasets"),
    ]

    # ------------------------------------------------------------------
    # Public method
    # ------------------------------------------------------------------

    def list_datasets(self) -> list[Data]:
        try:
            with httpx.Client(timeout=30) as client:
                token = self._get_access_token(client)
                datasets = self._fetch_datasets(client, token=token)
                result = [self._dataset_to_data(ds) for ds in datasets]
                self.status = result
                return result
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to list Power BI datasets."
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
    # Dataset listing
    # ------------------------------------------------------------------

    def _fetch_datasets(self, client: httpx.Client, *, token: str) -> list[dict]:
        endpoint = f"{_POWERBI_API_BASE}/groups/{self.workspace_id}/datasets"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            resp = client.get(endpoint, headers=headers)
            resp.raise_for_status()
            return resp.json().get("value", [])
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to fetch datasets from Power BI workspace."
            raise ValueError(msg) from exc

    @staticmethod
    def _dataset_to_data(ds: dict) -> Data:
        metadata = {
            "source": "power_bi",
            "dataset_id": ds.get("id"),
            "name": ds.get("name"),
            "configured_by": ds.get("configuredBy"),
            "is_refreshable": ds.get("isRefreshable"),
            "web_url": ds.get("webUrl"),
            "created_date": ds.get("createdDate"),
        }
        return Data(text=ds.get("name", ""), data=metadata)
