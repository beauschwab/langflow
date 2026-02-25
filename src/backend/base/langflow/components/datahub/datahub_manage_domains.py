"""DataHub Manage Domains component.

Set or unset the domain on DataHub entities.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import DropdownInput, MessageTextInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_SET_DOMAIN_MUTATION = """
mutation setDomain($domainUrn: String!, $entityUrn: String!) {
  setDomain(domainUrn: $domainUrn, entityUrn: $entityUrn)
}
"""

_UNSET_DOMAIN_MUTATION = """
mutation unsetDomain($entityUrn: String!) {
  unsetDomain(entityUrn: $entityUrn)
}
"""


class DataHubManageDomainsComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Manage Domains"
    description = "Set or unset the domain on DataHub entities to organize data assets under business domains."
    icon = "layout"
    name = "DataHubManageDomains"
    trace_type = "tool"

    inputs = [
        MessageTextInput(
            name="graphql_endpoint",
            display_name="GraphQL Endpoint",
            info="DataHub GraphQL API endpoint.",
            value="http://localhost:8080/api/graphql",
            required=True,
        ),
        SecretStrInput(
            name="access_token",
            display_name="Access Token",
            info="DataHub personal access token for authentication.",
            required=False,
        ),
        DropdownInput(
            name="action",
            display_name="Action",
            options=["set", "unset"],
            value="set",
            info="Whether to set or unset the domain.",
        ),
        MessageTextInput(
            name="domain_urn",
            display_name="Domain URN",
            info="The URN of the domain. Example: urn:li:domain:Finance. Required for 'set' action.",
            required=False,
        ),
        MessageTextInput(
            name="entity_urn",
            display_name="Entity URN",
            info="The URN of the entity to set the domain on.",
            required=True,
        ),
    ]

    class ManageDomainsSchema(BaseModel):
        action: str = Field(default="set", description="Action: 'set' or 'unset'.")
        domain_urn: str = Field(default="", description="URN of the domain. Example: urn:li:domain:Finance")
        entity_urn: str = Field(..., description="URN of the entity to set the domain on.")

    def _manage_domains(
        self,
        action: str = "set",
        domain_urn: str = "",
        entity_urn: str = "",
    ) -> list[Data]:
        if action == "set":
            if not domain_urn:
                msg = "domain_urn is required for 'set' action."
                raise ValueError(msg)
            self._execute_graphql(
                _SET_DOMAIN_MUTATION,
                {"domainUrn": domain_urn, "entityUrn": entity_urn},
            )
        else:
            self._execute_graphql(
                _UNSET_DOMAIN_MUTATION,
                {"entityUrn": entity_urn},
            )

        return [
            Data(
                text=f"Domain {action}: {domain_urn or '(removed)'} on {entity_urn}",
                data={
                    "urn": entity_urn,
                    "domain_urn": domain_urn or None,
                    "action": action,
                    "success": True,
                },
            )
        ]

    def run_model(self) -> list[Data]:
        return self._manage_domains(self.action, self.domain_urn or "", self.entity_urn)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_manage_domains",
            description="Set or unset the domain on DataHub entities to organize data assets under business domains.",
            func=self._manage_domains,
            args_schema=self.ManageDomainsSchema,
        )
