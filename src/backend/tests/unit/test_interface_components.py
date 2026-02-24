from langflow.interface.components import apply_enterprise_first_pass_component_filter


def test_apply_enterprise_first_pass_component_filter_excludes_bundle_types() -> None:
    all_types_dict = {
        "components": {
            "google": {"google_drive": {}},
            "confluence": {"confluence_loader": {}},
            "tools": {"datahub_graphql_mcp": {}},
        }
    }

    filtered = apply_enterprise_first_pass_component_filter(all_types_dict)

    assert "google" not in filtered["components"]
    assert "confluence" in filtered["components"]
    assert "confluence_loader" in filtered["components"]["confluence"]
    assert "tools" in filtered["components"]
    assert "datahub_graphql_mcp" in filtered["components"]["tools"]


def test_apply_enterprise_first_pass_component_filter_no_components_key() -> None:
    all_types_dict = {"other": {}}

    filtered = apply_enterprise_first_pass_component_filter(all_types_dict)

    assert filtered == all_types_dict


def test_apply_enterprise_first_pass_component_filter_with_non_dict_components() -> None:
    all_types_dict = {"components": ["not-a-dict"]}

    filtered = apply_enterprise_first_pass_component_filter(all_types_dict)

    assert filtered == all_types_dict


def test_apply_enterprise_first_pass_component_filter_with_custom_exclusions() -> None:
    all_types_dict = {"components": {"confluence": {"loader": {}}, "tools": {"datahub_graphql_mcp": {}}}}

    filtered = apply_enterprise_first_pass_component_filter(all_types_dict, excluded_component_types={"tools"})

    assert "confluence" in filtered["components"]
    assert "tools" not in filtered["components"]
