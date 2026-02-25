import json

import httpx

from langflow.custom import Component
from langflow.io import BoolInput, IntInput, Output, SecretStrInput, StrInput
from langflow.schema import Data

_POWERBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"
_POWERBI_API_BASE = "https://api.powerbi.com/v1.0/myorg"
_TOKEN_URL_TEMPLATE = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"


class PowerBIDAXQueryComponent(Component):
    """Execute a DAX query against a Power BI semantic model and return the result.

    Authenticates via Azure AD client-credentials flow.  The output is a
    ``list[Data]`` where each item represents one result table returned by the
    DAX engine, with each row's column values flattened into the *data* dict.
    This makes it straightforward to pipe results into downstream processing
    components (e.g. pandas via a Python component, chart generators, etc.).
    """

    display_name = "Power BI DAX Query"
    description = (
        "Execute a DAX query against a Power BI semantic model (dataset) and return the "
        "results as structured Data for further processing in a flow."
    )
    documentation = (
        "https://learn.microsoft.com/rest/api/power-bi/datasets/execute-queries-in-group"
    )
    trace_type = "tool"
    icon = "PowerBI"
    name = "PowerBIDAXQuery"

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
            info="Power BI workspace (group) ID that contains the semantic model.",
        ),
        StrInput(
            name="dataset_id",
            display_name="Dataset / Semantic Model ID",
            required=True,
            info="The unique ID of the Power BI dataset or semantic model to query.",
        ),
        StrInput(
            name="dax_query",
            display_name="DAX Query",
            required=True,
            info=(
                "DAX query to execute. Must start with a table constructor or EVALUATE. "
                "Example: EVALUATE SUMMARIZECOLUMNS('Date'[Year], \"Sales\", SUM(Sales[Amount]))"
            ),
        ),
        BoolInput(
            name="include_nulls",
            display_name="Include Nulls",
            value=True,
            advanced=True,
            info="When enabled, null values are included in the result set.",
        ),
        IntInput(
            name="max_rows",
            display_name="Max Rows",
            value=1000,
            advanced=True,
            info="Maximum number of rows to return per result table (1–100 000).",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Query Results", method="run_dax_query"),
    ]

    # ------------------------------------------------------------------
    # Public method
    # ------------------------------------------------------------------

    def run_dax_query(self) -> list[Data]:
        try:
            with httpx.Client(timeout=60) as client:
                token = self._get_access_token(client)
                rows = self._execute_dax(client, token=token)
                result = [Data(data=row) for row in rows]
                self.status = result
                return result
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            msg = "Power BI DAX query failed."
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
    # DAX execution
    # ------------------------------------------------------------------

    def _execute_dax(self, client: httpx.Client, *, token: str) -> list[dict]:
        endpoint = (
            f"{_POWERBI_API_BASE}/groups/{self.workspace_id}"
            f"/datasets/{self.dataset_id}/executeQueries"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        body = {
            "queries": [{"query": self.dax_query}],
            "serializerSettings": {"includeNulls": self.include_nulls},
        }
        try:
            resp = client.post(endpoint, headers=headers, content=json.dumps(body))
            resp.raise_for_status()
            return self._parse_response(resp.json())
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            msg = "Power BI DAX query execution failed. Check dataset ID and query syntax."
            raise ValueError(msg) from exc

    def _parse_response(self, payload: dict) -> list[dict]:
        """Flatten DAX result tables into a list of row dicts."""
        rows: list[dict] = []
        max_rows = max(1, int(self.max_rows or 1000))
        for table_result in payload.get("results", []):
            tables = table_result.get("tables", [])
            for table in tables:
                for row in table.get("rows", []):
                    if len(rows) >= max_rows:
                        break
                    # DAX column names use "[Table].[Column]" format — keep only the column part.
                    cleaned = {
                        k.rsplit(".", 1)[-1].strip("[]"): v
                        for k, v in row.items()
                    }
                    rows.append(cleaned)
                if len(rows) >= max_rows:
                    break
            if len(rows) >= max_rows:
                break
        return rows
