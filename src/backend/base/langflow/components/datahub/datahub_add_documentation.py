"""DataHub Add Documentation component.

Add or update documentation (description) on DataHub entities.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import MessageTextInput, MultilineInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_UPDATE_DESCRIPTION_MUTATION = """
mutation updateDescription($input: DescriptionUpdateInput!) {
  updateDescription(input: $input)
}
"""


class DataHubAddDocumentationComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Add Documentation"
    description = (
        "Add or update documentation (description) on a DataHub entity such as "
        "a dataset, dashboard, data job, or column."
    )
    icon = "DataHub"
    name = "DataHubAddDocumentation"
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
        MessageTextInput(
            name="entity_urn",
            display_name="Entity URN",
            info="The DataHub URN of the entity to document.",
            required=True,
        ),
        MultilineInput(
            name="documentation",
            display_name="Documentation",
            info="The documentation text (Markdown supported) to set on the entity.",
            required=True,
        ),
        MessageTextInput(
            name="sub_resource",
            display_name="Sub-Resource (optional)",
            info="Optional sub-resource path for column-level documentation (e.g., field path).",
            required=False,
            advanced=True,
        ),
    ]

    class AddDocumentationSchema(BaseModel):
        entity_urn: str = Field(..., description="DataHub URN of the entity to document.")
        documentation: str = Field(..., description="Documentation text (Markdown supported) to set on the entity.")
        sub_resource: str = Field(
            default="",
            description="Optional sub-resource path for column-level documentation (e.g., field path).",
        )

    def _add_documentation(
        self,
        entity_urn: str,
        documentation: str,
        sub_resource: str = "",
    ) -> list[Data]:
        variables: dict = {
            "input": {
                "description": documentation,
                "resourceUrn": entity_urn,
            },
        }
        if sub_resource:
            variables["input"]["subResourceType"] = "DATASET_FIELD"
            variables["input"]["subResource"] = sub_resource

        self._execute_graphql(_UPDATE_DESCRIPTION_MUTATION, variables)

        return [
            Data(
                text=f"Documentation updated for {entity_urn}",
                data={
                    "urn": entity_urn,
                    "action": "update_description",
                    "success": True,
                    "sub_resource": sub_resource or None,
                },
            )
        ]

    def run_model(self) -> list[Data]:
        return self._add_documentation(self.entity_urn, self.documentation, self.sub_resource or "")

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_add_documentation",
            description=(
                "Add or update documentation (description) on a DataHub entity. "
                "Supports entity-level and column-level documentation. Markdown is supported."
            ),
            func=self._add_documentation,
            args_schema=self.AddDocumentationSchema,
        )
