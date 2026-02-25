"""Unit tests for the DataHub component bundle.

Tests cover default configuration, frontend node rendering, tool building,
and GraphQL execution logic (with mocked HTTP transport).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from langflow.components.datahub import (
    DataHubAddDocumentationComponent,
    DataHubGetMetadataComponent,
    DataHubLineageComponent,
    DataHubManageDomainsComponent,
    DataHubManagePropertiesComponent,
    DataHubManageTagsComponent,
    DataHubManageTermsComponent,
    DataHubSearchComponent,
)


# ---------------------------------------------------------------------------
# Defaults / frontend-node tests
# ---------------------------------------------------------------------------


class TestDataHubSearchDefaults:
    def test_display_name_and_inputs(self):
        component = DataHubSearchComponent()
        node = component.to_frontend_node()
        node_data = node["data"]["node"]
        template = node_data["template"]

        assert node_data["display_name"] == "DataHub Search"
        assert template["graphql_endpoint"]["value"] == "http://localhost:8080/api/graphql"
        assert template["entity_type"]["value"] == "ALL"
        assert template["max_results"]["value"] == 10


class TestDataHubGetMetadataDefaults:
    def test_display_name_and_inputs(self):
        component = DataHubGetMetadataComponent()
        node = component.to_frontend_node()
        node_data = node["data"]["node"]

        assert node_data["display_name"] == "DataHub Get Metadata"
        assert "entity_urn" in node_data["template"]


class TestDataHubLineageDefaults:
    def test_display_name_and_inputs(self):
        component = DataHubLineageComponent()
        node = component.to_frontend_node()
        node_data = node["data"]["node"]
        template = node_data["template"]

        assert node_data["display_name"] == "DataHub Lineage"
        assert template["direction"]["value"] == "DOWNSTREAM"
        assert template["max_hops"]["value"] == 3


class TestDataHubWriteComponentDefaults:
    @pytest.mark.parametrize(
        ("cls", "expected_name"),
        [
            (DataHubAddDocumentationComponent, "DataHub Add Documentation"),
            (DataHubManageTagsComponent, "DataHub Manage Tags"),
            (DataHubManageTermsComponent, "DataHub Manage Glossary Terms"),
            (DataHubManageDomainsComponent, "DataHub Manage Domains"),
            (DataHubManagePropertiesComponent, "DataHub Manage Structured Properties"),
        ],
    )
    def test_display_names(self, cls, expected_name):
        component = cls()
        node = component.to_frontend_node()
        assert node["data"]["node"]["display_name"] == expected_name


# ---------------------------------------------------------------------------
# Tool build tests
# ---------------------------------------------------------------------------


class TestToolBuilding:
    @pytest.mark.parametrize(
        ("cls", "expected_tool_name"),
        [
            (DataHubSearchComponent, "datahub_search"),
            (DataHubGetMetadataComponent, "datahub_get_metadata"),
            (DataHubLineageComponent, "datahub_lineage"),
            (DataHubAddDocumentationComponent, "datahub_add_documentation"),
            (DataHubManageTagsComponent, "datahub_manage_tags"),
            (DataHubManageTermsComponent, "datahub_manage_terms"),
            (DataHubManageDomainsComponent, "datahub_manage_domains"),
            (DataHubManagePropertiesComponent, "datahub_manage_properties"),
        ],
    )
    def test_build_tool_returns_named_tool(self, cls, expected_tool_name):
        component = cls()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = ""
        tool = component.build_tool()
        assert tool.name == expected_tool_name
        assert tool.description


# ---------------------------------------------------------------------------
# GraphQL execution tests (mocked HTTP)
# ---------------------------------------------------------------------------

def _mock_httpx_post(json_response):
    """Return a context-manager mock that yields a client whose .post returns *json_response*."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.json.return_value = json_response
    mock_response.raise_for_status = MagicMock()

    mock_client = MagicMock()
    mock_client.post.return_value = mock_response
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    return mock_client


class TestSearchExecution:
    def test_search_returns_results(self):
        component = DataHubSearchComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = "test-token"
        component.search_query = "customer"
        component.entity_type = "DATASET"
        component.max_results = 5

        gql_response = {
            "data": {
                "search": {
                    "start": 0,
                    "count": 1,
                    "total": 1,
                    "searchResults": [
                        {
                            "entity": {
                                "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.customers,PROD)",
                                "type": "DATASET",
                                "name": "customers",
                                "platform": {"name": "snowflake"},
                                "properties": {
                                    "description": "Customer master data",
                                    "qualifiedName": "db.schema.customers",
                                },
                            },
                            "matchedFields": [{"name": "name", "value": "customers"}],
                        }
                    ],
                }
            }
        }

        mock_client = _mock_httpx_post(gql_response)
        with patch("httpx.Client", return_value=mock_client):
            results = component.run_model()

        assert len(results) == 1
        assert results[0].data["urn"] == "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.customers,PROD)"
        assert results[0].data["name"] == "customers"
        assert results[0].data["platform"] == "snowflake"


class TestGetMetadataExecution:
    def test_get_metadata_returns_entity(self):
        component = DataHubGetMetadataComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = "test-token"
        component.entity_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.customers,PROD)"

        gql_response = {
            "data": {
                "entity": {
                    "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.customers,PROD)",
                    "type": "DATASET",
                    "name": "customers",
                    "platform": {"name": "snowflake"},
                    "properties": {
                        "name": "customers",
                        "qualifiedName": "db.schema.customers",
                        "description": "Customer data",
                        "customProperties": [{"key": "team", "value": "analytics"}],
                        "created": {"time": 1700000000000},
                        "lastModified": {"time": 1700100000000},
                    },
                    "editableProperties": {"description": "Editable desc"},
                    "schemaMetadata": {
                        "fields": [
                            {
                                "fieldPath": "customer_id",
                                "type": "NUMBER",
                                "nativeDataType": "INT",
                                "description": "Primary key",
                                "nullable": False,
                            }
                        ]
                    },
                    "ownership": {
                        "owners": [
                            {
                                "owner": {"urn": "urn:li:corpuser:john", "type": "CORP_USER", "username": "john"},
                                "ownershipType": {"name": "DATAOWNER"},
                            }
                        ]
                    },
                    "tags": {"tags": [{"tag": {"urn": "urn:li:tag:PII", "properties": {"name": "PII", "description": ""}}}]},
                    "glossaryTerms": {"terms": [{"term": {"urn": "urn:li:glossaryTerm:Customer", "properties": {"name": "Customer", "description": ""}}}]},
                    "domain": {"domain": {"urn": "urn:li:domain:Commerce", "properties": {"name": "Commerce", "description": ""}}},
                    "deprecation": {"deprecated": False, "note": ""},
                    "subTypes": {"typeNames": ["table"]},
                }
            }
        }

        mock_client = _mock_httpx_post(gql_response)
        with patch("httpx.Client", return_value=mock_client):
            results = component.run_model()

        assert len(results) == 1
        data = results[0].data
        assert data["name"] == "customers"
        assert data["platform"] == "snowflake"
        assert len(data["schema_fields"]) == 1
        assert data["schema_fields"][0]["field_path"] == "customer_id"
        assert len(data["owners"]) == 1
        assert data["owners"][0]["name"] == "john"
        assert len(data["tags"]) == 1
        assert data["tags"][0]["name"] == "PII"
        assert data["domain"]["name"] == "Commerce"
        assert data["custom_properties"]["team"] == "analytics"


class TestLineageExecution:
    def test_lineage_returns_graph(self):
        component = DataHubLineageComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = ""
        component.entity_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.customers,PROD)"
        component.direction = "DOWNSTREAM"
        component.max_hops = 2
        component.max_results = 10

        gql_response = {
            "data": {
                "searchAcrossLineage": {
                    "start": 0,
                    "count": 1,
                    "total": 1,
                    "searchResults": [
                        {
                            "entity": {
                                "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.orders,PROD)",
                                "type": "DATASET",
                                "name": "orders",
                                "platform": {"name": "snowflake"},
                                "properties": {"name": "orders", "description": "Order data", "qualifiedName": "db.schema.orders"},
                            },
                            "paths": [{"path": [{"urn": "urn:li:dataset:customers", "type": "DATASET"}]}],
                            "degree": 1,
                        }
                    ],
                }
            }
        }

        mock_client = _mock_httpx_post(gql_response)
        with patch("httpx.Client", return_value=mock_client):
            results = component.run_model()

        assert len(results) == 1
        assert results[0].data["name"] == "orders"
        assert results[0].data["degree"] == 1
        assert results[0].data["direction"] == "DOWNSTREAM"


class TestAddDocumentationExecution:
    def test_add_documentation_success(self):
        component = DataHubAddDocumentationComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = "test-token"
        component.entity_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.customers,PROD)"
        component.documentation = "# Customer Data\nThis is the customer master table."
        component.sub_resource = ""

        gql_response = {"data": {"updateDescription": True}}

        mock_client = _mock_httpx_post(gql_response)
        with patch("httpx.Client", return_value=mock_client):
            results = component.run_model()

        assert len(results) == 1
        assert results[0].data["success"] is True
        assert results[0].data["action"] == "update_description"


class TestManageTagsExecution:
    def test_add_tag_success(self):
        component = DataHubManageTagsComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = "test-token"
        component.action = "add"
        component.tag_urn = "urn:li:tag:PII"
        component.entity_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.customers,PROD)"
        component.sub_resource = ""

        gql_response = {"data": {"addTag": True}}

        mock_client = _mock_httpx_post(gql_response)
        with patch("httpx.Client", return_value=mock_client):
            results = component.run_model()

        assert len(results) == 1
        assert results[0].data["success"] is True
        assert results[0].data["tag_urn"] == "urn:li:tag:PII"


class TestManageDomainsExecution:
    def test_set_domain_requires_urn(self):
        component = DataHubManageDomainsComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = ""
        component.action = "set"
        component.domain_urn = ""
        component.entity_urn = "urn:li:dataset:test"

        with pytest.raises(ValueError, match="domain_urn is required"):
            component.run_model()

    def test_set_domain_success(self):
        component = DataHubManageDomainsComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = ""
        component.action = "set"
        component.domain_urn = "urn:li:domain:Finance"
        component.entity_urn = "urn:li:dataset:test"

        gql_response = {"data": {"setDomain": True}}

        mock_client = _mock_httpx_post(gql_response)
        with patch("httpx.Client", return_value=mock_client):
            results = component.run_model()

        assert len(results) == 1
        assert results[0].data["success"] is True
        assert results[0].data["domain_urn"] == "urn:li:domain:Finance"


class TestManagePropertiesExecution:
    def test_upsert_requires_values(self):
        component = DataHubManagePropertiesComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = ""
        component.action = "upsert"
        component.entity_urn = "urn:li:dataset:test"
        component.property_urn = "urn:li:structuredProperty:retention"
        component.property_values = ""

        with pytest.raises(ValueError, match="property_values is required"):
            component.run_model()


class TestGraphQLErrorHandling:
    def test_graphql_errors_raise_valueerror(self):
        component = DataHubSearchComponent()
        component.graphql_endpoint = "http://localhost:8080/api/graphql"
        component.access_token = ""
        component.search_query = "test"
        component.entity_type = "ALL"
        component.max_results = 10

        gql_response = {"errors": [{"message": "Unauthorized"}]}

        mock_client = _mock_httpx_post(gql_response)
        with patch("httpx.Client", return_value=mock_client), pytest.raises(ValueError, match="GraphQL errors"):
            component.run_model()
