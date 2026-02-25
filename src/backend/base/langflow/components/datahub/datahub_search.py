"""DataHub Search component.

Search across all DataHub entities using keywords and optional filters.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import DropdownInput, IntInput, MessageTextInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_SEARCH_QUERY = """
query search($input: SearchInput!) {
  search(input: $input) {
    start
    count
    total
    searchResults {
      entity {
        urn
        type
        ... on Dataset {
          name
          platform { name }
          properties { description qualifiedName }
        }
        ... on Dashboard {
          urn
          properties { name description }
        }
        ... on DataJob {
          urn
          properties { name description }
        }
        ... on DataFlow {
          urn
          properties { name description }
        }
        ... on GlossaryTerm {
          urn
          properties { name description }
        }
      }
      matchedFields {
        name
        value
      }
    }
  }
}
"""


class DataHubSearchComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Search"
    description = "Search across DataHub entities (datasets, dashboards, data jobs, glossary terms, etc.) using keywords and optional filters."
    icon = "DataHub"
    name = "DataHubSearch"
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
            name="search_query",
            display_name="Search Query",
            info="Keywords to search for across DataHub entities.",
            required=True,
        ),
        DropdownInput(
            name="entity_type",
            display_name="Entity Type",
            options=["ALL", "DATASET", "DASHBOARD", "DATA_JOB", "DATA_FLOW", "GLOSSARY_TERM", "CONTAINER", "DOMAIN"],
            value="ALL",
            info="Filter results by entity type.",
        ),
        IntInput(
            name="max_results",
            display_name="Max Results",
            value=10,
            info="Maximum number of results to return (1-100).",
            advanced=True,
        ),
    ]

    class SearchSchema(BaseModel):
        search_query: str = Field(..., description="Keywords to search for across DataHub entities.")
        entity_type: str = Field(
            default="ALL",
            description="Entity type filter: ALL, DATASET, DASHBOARD, DATA_JOB, DATA_FLOW, GLOSSARY_TERM, CONTAINER, or DOMAIN.",
        )
        max_results: int = Field(default=10, description="Maximum number of results (1-100).")

    def _search(self, search_query: str, entity_type: str = "ALL", max_results: int = 10) -> list[Data]:
        variables: dict = {
            "input": {
                "type": entity_type if entity_type != "ALL" else "",
                "query": search_query,
                "start": 0,
                "count": max(1, min(int(max_results), 100)),
            },
        }
        if entity_type == "ALL":
            variables["input"].pop("type")

        data = self._execute_graphql(_SEARCH_QUERY, variables)
        search_data = data.get("search", {})

        results: list[Data] = []
        for item in search_data.get("searchResults", []):
            entity = item.get("entity", {})
            props = entity.get("properties", {})
            matched = item.get("matchedFields", [])
            results.append(
                Data(
                    text=props.get("description", "") or props.get("name", "") or entity.get("name", ""),
                    data={
                        "urn": entity.get("urn"),
                        "type": entity.get("type"),
                        "name": entity.get("name") or props.get("name", ""),
                        "qualified_name": props.get("qualifiedName", ""),
                        "description": props.get("description", ""),
                        "platform": (entity.get("platform") or {}).get("name", ""),
                        "matched_fields": [{"name": m.get("name"), "value": m.get("value")} for m in matched],
                    },
                )
            )
        return results

    def run_model(self) -> list[Data]:
        return self._search(self.search_query, self.entity_type, self.max_results)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_search",
            description=(
                "Search across DataHub entities (datasets, dashboards, data jobs, glossary terms) "
                "using keywords and optional entity type filter."
            ),
            func=self._search,
            args_schema=self.SearchSchema,
        )
