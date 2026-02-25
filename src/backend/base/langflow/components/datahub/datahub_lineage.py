"""DataHub Lineage component.

Explore upstream and downstream lineage for any DataHub entity.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import DropdownInput, IntInput, MessageTextInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_LINEAGE_QUERY = """
query searchAcrossLineage($input: SearchAcrossLineageInput!) {
  searchAcrossLineage(input: $input) {
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
          properties { name description qualifiedName }
        }
        ... on DataJob {
          urn
          properties { name description }
        }
        ... on DataFlow {
          urn
          properties { name description }
        }
        ... on Dashboard {
          urn
          properties { name description }
        }
      }
      paths {
        path {
          urn
          type
        }
      }
      degree
    }
  }
}
"""


class DataHubLineageComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Lineage"
    description = (
        "Explore upstream and downstream data lineage for a DataHub entity. "
        "Navigate multi-hop lineage across data pipelines to understand data flows and impact."
    )
    icon = "DataHub"
    name = "DataHubLineage"
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
            info="The DataHub URN of the entity to explore lineage for.",
            required=True,
        ),
        DropdownInput(
            name="direction",
            display_name="Direction",
            options=["UPSTREAM", "DOWNSTREAM"],
            value="DOWNSTREAM",
            info="Lineage direction: UPSTREAM (dependencies) or DOWNSTREAM (dependents).",
        ),
        IntInput(
            name="max_hops",
            display_name="Max Hops",
            value=3,
            info="Maximum number of hops to traverse (1-10).",
            advanced=True,
        ),
        IntInput(
            name="max_results",
            display_name="Max Results",
            value=20,
            info="Maximum number of lineage results to return.",
            advanced=True,
        ),
    ]

    class LineageSchema(BaseModel):
        entity_urn: str = Field(..., description="DataHub URN of the entity to explore lineage for.")
        direction: str = Field(
            default="DOWNSTREAM",
            description="Lineage direction: UPSTREAM (dependencies) or DOWNSTREAM (dependents).",
        )
        max_hops: int = Field(default=3, description="Maximum number of hops to traverse (1-10).")
        max_results: int = Field(default=20, description="Maximum number of lineage results to return.")

    def _get_lineage(
        self,
        entity_urn: str,
        direction: str = "DOWNSTREAM",
        max_hops: int = 3,
        max_results: int = 20,
    ) -> list[Data]:
        variables = {
            "input": {
                "urn": entity_urn,
                "direction": direction,
                "orFilters": [],
                "start": 0,
                "count": max(1, min(int(max_results), 100)),
            },
        }
        if max_hops:
            variables["input"]["maxHops"] = max(1, min(int(max_hops), 10))

        data = self._execute_graphql(_LINEAGE_QUERY, variables)
        lineage_data = data.get("searchAcrossLineage", {})

        results: list[Data] = []
        for item in lineage_data.get("searchResults", []):
            entity = item.get("entity", {})
            props = entity.get("properties") or {}
            paths = item.get("paths", [])
            degree = item.get("degree")

            path_list = []
            for p in paths:
                path_list.append([
                    {"urn": node.get("urn"), "type": node.get("type")}
                    for node in p.get("path", [])
                ])

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
                        "degree": degree,
                        "direction": direction,
                        "paths": path_list,
                    },
                )
            )
        return results

    def run_model(self) -> list[Data]:
        return self._get_lineage(self.entity_urn, self.direction, self.max_hops, self.max_results)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_lineage",
            description=(
                "Explore upstream or downstream data lineage for a DataHub entity. "
                "Traverse multi-hop lineage to understand data flows, dependencies, and impact analysis."
            ),
            func=self._get_lineage,
            args_schema=self.LineageSchema,
        )
