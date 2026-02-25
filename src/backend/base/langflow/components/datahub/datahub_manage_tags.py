"""DataHub Manage Tags component.

Add or remove tags on DataHub entities.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import DropdownInput, MessageTextInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_ADD_TAG_MUTATION = """
mutation addTag($input: TagAssociationInput!) {
  addTag(input: $input)
}
"""

_REMOVE_TAG_MUTATION = """
mutation removeTag($input: TagAssociationInput!) {
  removeTag(input: $input)
}
"""


class DataHubManageTagsComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Manage Tags"
    description = "Add or remove tags on DataHub entities such as datasets, dashboards, or columns."
    icon = "DataHub"
    name = "DataHubManageTags"
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
            options=["add", "remove"],
            value="add",
            info="Whether to add or remove the tag.",
        ),
        MessageTextInput(
            name="tag_urn",
            display_name="Tag URN",
            info="The URN of the tag. Example: urn:li:tag:PII",
            required=True,
        ),
        MessageTextInput(
            name="entity_urn",
            display_name="Entity URN",
            info="The URN of the entity to tag.",
            required=True,
        ),
        MessageTextInput(
            name="sub_resource",
            display_name="Sub-Resource (optional)",
            info="Optional sub-resource path for column-level tagging (e.g., field path).",
            required=False,
            advanced=True,
        ),
    ]

    class ManageTagsSchema(BaseModel):
        action: str = Field(default="add", description="Action: 'add' or 'remove'.")
        tag_urn: str = Field(..., description="URN of the tag. Example: urn:li:tag:PII")
        entity_urn: str = Field(..., description="URN of the entity to tag.")
        sub_resource: str = Field(
            default="",
            description="Optional sub-resource path for column-level tagging.",
        )

    def _manage_tags(
        self,
        action: str = "add",
        tag_urn: str = "",
        entity_urn: str = "",
        sub_resource: str = "",
    ) -> list[Data]:
        mutation = _ADD_TAG_MUTATION if action == "add" else _REMOVE_TAG_MUTATION

        variables: dict = {
            "input": {
                "tagUrn": tag_urn,
                "resourceUrn": entity_urn,
            },
        }
        if sub_resource:
            variables["input"]["subResourceType"] = "DATASET_FIELD"
            variables["input"]["subResource"] = sub_resource

        self._execute_graphql(mutation, variables)

        return [
            Data(
                text=f"Tag {action}{'d' if action == 'add' else 'd'}: {tag_urn} on {entity_urn}",
                data={
                    "urn": entity_urn,
                    "tag_urn": tag_urn,
                    "action": action,
                    "success": True,
                    "sub_resource": sub_resource or None,
                },
            )
        ]

    def run_model(self) -> list[Data]:
        return self._manage_tags(self.action, self.tag_urn, self.entity_urn, self.sub_resource or "")

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_manage_tags",
            description="Add or remove tags on DataHub entities (datasets, dashboards, columns).",
            func=self._manage_tags,
            args_schema=self.ManageTagsSchema,
        )
