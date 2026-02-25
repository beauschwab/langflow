"""DataHub Manage Structured Properties component.

Upsert or remove structured properties on DataHub entities.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import DropdownInput, MessageTextInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_UPSERT_PROPERTIES_MUTATION = """
mutation upsertStructuredProperties($input: UpsertStructuredPropertiesInput!) {
  upsertStructuredProperties(input: $input)
}
"""

_REMOVE_PROPERTIES_MUTATION = """
mutation removeStructuredProperties($input: RemoveStructuredPropertiesInput!) {
  removeStructuredProperties(input: $input)
}
"""


class DataHubManagePropertiesComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Manage Structured Properties"
    description = (
        "Upsert or remove structured properties on DataHub entities for custom metadata enrichment."
    )
    icon = "DataHub"
    name = "DataHubManageProperties"
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
            options=["upsert", "remove"],
            value="upsert",
            info="Whether to upsert or remove the structured property.",
        ),
        MessageTextInput(
            name="entity_urn",
            display_name="Entity URN",
            info="The URN of the entity to update properties on.",
            required=True,
        ),
        MessageTextInput(
            name="property_urn",
            display_name="Property URN",
            info="The URN of the structured property definition. Example: urn:li:structuredProperty:retentionTime",
            required=True,
        ),
        MessageTextInput(
            name="property_values",
            display_name="Property Values",
            info="Comma-separated values to set for the structured property. Required for 'upsert' action.",
            required=False,
        ),
    ]

    class ManagePropertiesSchema(BaseModel):
        action: str = Field(default="upsert", description="Action: 'upsert' or 'remove'.")
        entity_urn: str = Field(..., description="URN of the entity to update properties on.")
        property_urn: str = Field(
            ...,
            description="URN of the structured property. Example: urn:li:structuredProperty:retentionTime",
        )
        property_values: str = Field(
            default="",
            description="Comma-separated values for the property. Required for 'upsert'.",
        )

    def _manage_properties(
        self,
        action: str = "upsert",
        entity_urn: str = "",
        property_urn: str = "",
        property_values: str = "",
    ) -> list[Data]:
        if action == "upsert":
            if not property_values:
                msg = "property_values is required for 'upsert' action."
                raise ValueError(msg)
            values = [v.strip() for v in property_values.split(",") if v.strip()]
            self._execute_graphql(
                _UPSERT_PROPERTIES_MUTATION,
                {
                    "input": {
                        "assetUrn": entity_urn,
                        "structuredPropertyInputParams": [
                            {
                                "structuredPropertyUrn": property_urn,
                                "values": [{"stringValue": v} for v in values],
                            },
                        ],
                    },
                },
            )
        else:
            self._execute_graphql(
                _REMOVE_PROPERTIES_MUTATION,
                {
                    "input": {
                        "assetUrn": entity_urn,
                        "structuredPropertyUrns": [property_urn],
                    },
                },
            )

        return [
            Data(
                text=f"Structured property {action}: {property_urn} on {entity_urn}",
                data={
                    "urn": entity_urn,
                    "property_urn": property_urn,
                    "action": action,
                    "success": True,
                    "values": property_values if action == "upsert" else None,
                },
            )
        ]

    def run_model(self) -> list[Data]:
        return self._manage_properties(
            self.action, self.entity_urn, self.property_urn, self.property_values or ""
        )

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_manage_properties",
            description="Upsert or remove structured properties on DataHub entities for custom metadata enrichment.",
            func=self._manage_properties,
            args_schema=self.ManagePropertiesSchema,
        )
