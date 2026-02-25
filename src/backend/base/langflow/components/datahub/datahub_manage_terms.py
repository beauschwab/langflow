"""DataHub Manage Glossary Terms component.

Add or remove glossary terms on DataHub entities.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import DropdownInput, MessageTextInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_ADD_TERM_MUTATION = """
mutation addTerm($input: TermAssociationInput!) {
  addTerm(input: $input)
}
"""

_REMOVE_TERM_MUTATION = """
mutation removeTerm($input: TermAssociationInput!) {
  removeTerm(input: $input)
}
"""


class DataHubManageTermsComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Manage Glossary Terms"
    description = (
        "Add or remove glossary terms on DataHub entities to maintain business vocabulary "
        "and data governance standards."
    )
    icon = "DataHub"
    name = "DataHubManageTerms"
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
            info="Whether to add or remove the glossary term.",
        ),
        MessageTextInput(
            name="term_urn",
            display_name="Glossary Term URN",
            info="The URN of the glossary term. Example: urn:li:glossaryTerm:CustomerID",
            required=True,
        ),
        MessageTextInput(
            name="entity_urn",
            display_name="Entity URN",
            info="The URN of the entity to associate the term with.",
            required=True,
        ),
        MessageTextInput(
            name="sub_resource",
            display_name="Sub-Resource (optional)",
            info="Optional sub-resource path for column-level term association (e.g., field path).",
            required=False,
            advanced=True,
        ),
    ]

    class ManageTermsSchema(BaseModel):
        action: str = Field(default="add", description="Action: 'add' or 'remove'.")
        term_urn: str = Field(..., description="URN of the glossary term. Example: urn:li:glossaryTerm:CustomerID")
        entity_urn: str = Field(..., description="URN of the entity to associate the term with.")
        sub_resource: str = Field(
            default="",
            description="Optional sub-resource path for column-level association.",
        )

    def _manage_terms(
        self,
        action: str = "add",
        term_urn: str = "",
        entity_urn: str = "",
        sub_resource: str = "",
    ) -> list[Data]:
        mutation = _ADD_TERM_MUTATION if action == "add" else _REMOVE_TERM_MUTATION

        variables: dict = {
            "input": {
                "termUrn": term_urn,
                "resourceUrn": entity_urn,
            },
        }
        if sub_resource:
            variables["input"]["subResourceType"] = "DATASET_FIELD"
            variables["input"]["subResource"] = sub_resource

        self._execute_graphql(mutation, variables)

        return [
            Data(
                text=f"Glossary term {action}{'d' if action == 'add' else 'd'}: {term_urn} on {entity_urn}",
                data={
                    "urn": entity_urn,
                    "term_urn": term_urn,
                    "action": action,
                    "success": True,
                    "sub_resource": sub_resource or None,
                },
            )
        ]

    def run_model(self) -> list[Data]:
        return self._manage_terms(self.action, self.term_urn, self.entity_urn, self.sub_resource or "")

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_manage_terms",
            description=(
                "Add or remove glossary terms on DataHub entities to maintain business vocabulary "
                "and data governance standards."
            ),
            func=self._manage_terms,
            args_schema=self.ManageTermsSchema,
        )
