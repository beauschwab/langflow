"""DataHub Get Metadata component.

Retrieve comprehensive metadata for any DataHub entity by its URN.
"""

from __future__ import annotations

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.field_typing import Tool
from langflow.inputs import MessageTextInput, SecretStrInput
from langflow.schema import Data

from .datahub_base import DataHubGraphQLMixin

_GET_ENTITY_QUERY = """
query getEntity($urn: String!) {
  entity(urn: $urn) {
    urn
    type
    ... on Dataset {
      name
      platform { name }
      properties {
        name
        qualifiedName
        description
        customProperties { key value }
        created { time }
        lastModified { time }
      }
      editableProperties { description }
      schemaMetadata {
        fields {
          fieldPath
          nativeDataType
          type
          description
          nullable
        }
      }
      ownership {
        owners {
          owner {
            urn
            type
            ... on CorpUser { username }
            ... on CorpGroup { name }
          }
          ownershipType { name }
        }
      }
      tags {
        tags {
          tag { urn properties { name description } }
        }
      }
      glossaryTerms {
        terms {
          term { urn properties { name description } }
        }
      }
      domain {
        domain { urn properties { name description } }
      }
      deprecation { deprecated note }
      subTypes { typeNames }
    }
    ... on Dashboard {
      urn
      properties { name description externalUrl }
      ownership {
        owners {
          owner { urn type ... on CorpUser { username } }
        }
      }
      tags { tags { tag { urn properties { name } } } }
    }
    ... on GlossaryTerm {
      urn
      properties { name description }
      parentNodes { nodes { urn properties { name } } }
    }
  }
}
"""


class DataHubGetMetadataComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub Get Metadata"
    description = (
        "Retrieve comprehensive metadata for any DataHub entity by its URN, "
        "including schema, ownership, tags, glossary terms, domain, and documentation."
    )
    icon = "DataHub"
    name = "DataHubGetMetadata"
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
            info="The DataHub URN of the entity to retrieve. Example: urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.table,PROD)",
            required=True,
        ),
    ]

    class GetMetadataSchema(BaseModel):
        entity_urn: str = Field(
            ...,
            description="DataHub URN of the entity. Example: urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.table,PROD)",
        )

    def _get_metadata(self, entity_urn: str) -> list[Data]:
        data = self._execute_graphql(_GET_ENTITY_QUERY, {"urn": entity_urn})
        entity = data.get("entity", {})
        if not entity:
            return [Data(text="Entity not found", data={"urn": entity_urn, "error": "Entity not found"})]

        props = entity.get("properties") or {}
        editable = entity.get("editableProperties") or {}
        schema_meta = entity.get("schemaMetadata") or {}

        fields = []
        for f in schema_meta.get("fields", []):
            fields.append({
                "field_path": f.get("fieldPath"),
                "type": f.get("type"),
                "native_type": f.get("nativeDataType"),
                "description": f.get("description", ""),
                "nullable": f.get("nullable"),
            })

        owners = []
        for o in (entity.get("ownership") or {}).get("owners", []):
            owner = o.get("owner", {})
            owners.append({
                "urn": owner.get("urn"),
                "name": owner.get("username") or owner.get("name", ""),
                "type": (o.get("ownershipType") or {}).get("name", ""),
            })

        tags = [
            {
                "urn": t["tag"].get("urn"),
                "name": (t["tag"].get("properties") or {}).get("name", ""),
            }
            for t in (entity.get("tags") or {}).get("tags", [])
        ]

        terms = [
            {
                "urn": t["term"].get("urn"),
                "name": (t["term"].get("properties") or {}).get("name", ""),
            }
            for t in (entity.get("glossaryTerms") or {}).get("terms", [])
        ]

        domain_info = (entity.get("domain") or {}).get("domain")
        domain = None
        if domain_info:
            domain = {
                "urn": domain_info.get("urn"),
                "name": (domain_info.get("properties") or {}).get("name", ""),
            }

        deprecation = entity.get("deprecation") or {}
        custom_props = {
            p["key"]: p["value"] for p in props.get("customProperties", [])
        }

        description = editable.get("description") or props.get("description", "")

        result = {
            "urn": entity.get("urn"),
            "type": entity.get("type"),
            "name": entity.get("name") or props.get("name", ""),
            "qualified_name": props.get("qualifiedName", ""),
            "description": description,
            "platform": (entity.get("platform") or {}).get("name", ""),
            "schema_fields": fields,
            "owners": owners,
            "tags": tags,
            "glossary_terms": terms,
            "domain": domain,
            "sub_types": (entity.get("subTypes") or {}).get("typeNames", []),
            "deprecated": deprecation.get("deprecated", False),
            "deprecation_note": deprecation.get("note", ""),
            "custom_properties": custom_props,
            "created": (props.get("created") or {}).get("time"),
            "last_modified": (props.get("lastModified") or {}).get("time"),
        }

        return [Data(text=description, data=result)]

    def run_model(self) -> list[Data]:
        return self._get_metadata(self.entity_urn)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_get_metadata",
            description=(
                "Retrieve comprehensive metadata for a DataHub entity by its URN, "
                "including schema, ownership, tags, glossary terms, domain, and documentation."
            ),
            func=self._get_metadata,
            args_schema=self.GetMetadataSchema,
        )
