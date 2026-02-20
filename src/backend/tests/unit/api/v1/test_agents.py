from fastapi import status
from httpx import AsyncClient


async def test_create_agent(client: AsyncClient, logged_in_headers):
    basic_case = {
        "name": "test-agent",
        "description": "A test agent",
        "agent_type": "tool_calling",
        "config": {"max_iterations": 10},
        "tools": ["calculator", "search"],
        "tags": ["test"],
    }
    response = await client.post("api/v1/agents/", json=basic_case, headers=logged_in_headers)
    result = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(result, dict), "The result must be a dictionary"
    assert "id" in result, "The result must have an 'id' key"
    assert "name" in result, "The result must have a 'name' key"
    assert "description" in result, "The result must have a 'description' key"
    assert "agent_type" in result, "The result must have an 'agent_type' key"
    assert "config" in result, "The result must have a 'config' key"
    assert "tools" in result, "The result must have a 'tools' key"
    assert "tags" in result, "The result must have a 'tags' key"
    assert "user_id" in result, "The result must have a 'user_id' key"
    assert "updated_at" in result, "The result must have an 'updated_at' key"
    assert result["name"] == "test-agent"
    assert result["description"] == "A test agent"
    assert result["agent_type"] == "tool_calling"
    assert result["config"] == {"max_iterations": 10}
    assert result["tools"] == ["calculator", "search"]


async def test_read_agents(client: AsyncClient, logged_in_headers):
    # Create an agent first
    agent_data = {
        "name": "list-test-agent",
        "description": "Agent for list test",
    }
    await client.post("api/v1/agents/", json=agent_data, headers=logged_in_headers)

    response = await client.get("api/v1/agents/", headers=logged_in_headers)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(result, list), "The result must be a list"
    assert len(result) >= 1, "There must be at least one agent"


async def test_read_agents_with_search(client: AsyncClient, logged_in_headers):
    # Create agents
    await client.post(
        "api/v1/agents/",
        json={"name": "search-alpha-agent", "description": "Alpha"},
        headers=logged_in_headers,
    )
    await client.post(
        "api/v1/agents/",
        json={"name": "search-beta-agent", "description": "Beta"},
        headers=logged_in_headers,
    )

    response = await client.get("api/v1/agents/", params={"search": "alpha"}, headers=logged_in_headers)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(result, list)
    assert all("alpha" in a["name"].lower() for a in result)


async def test_read_agent(client: AsyncClient, logged_in_headers):
    # Create an agent first
    agent_data = {
        "name": "read-test-agent",
        "description": "Agent for read test",
        "agent_type": "lc_agent",
    }
    create_response = await client.post("api/v1/agents/", json=agent_data, headers=logged_in_headers)
    agent_id = create_response.json()["id"]

    response = await client.get(f"api/v1/agents/{agent_id}", headers=logged_in_headers)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["id"] == agent_id
    assert result["name"] == "read-test-agent"
    assert result["agent_type"] == "lc_agent"


async def test_update_agent(client: AsyncClient, logged_in_headers):
    # Create an agent first
    agent_data = {
        "name": "update-test-agent",
        "description": "Agent for update test",
    }
    create_response = await client.post("api/v1/agents/", json=agent_data, headers=logged_in_headers)
    agent_id = create_response.json()["id"]

    # Update the agent
    update_data = {
        "name": "updated-agent",
        "description": "Updated description",
        "config": {"temperature": 0.7},
    }
    response = await client.patch(f"api/v1/agents/{agent_id}", json=update_data, headers=logged_in_headers)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["name"] == "updated-agent"
    assert result["description"] == "Updated description"
    assert result["config"] == {"temperature": 0.7}


async def test_delete_agent(client: AsyncClient, logged_in_headers):
    # Create an agent first
    agent_data = {
        "name": "delete-test-agent",
        "description": "Agent for delete test",
    }
    create_response = await client.post("api/v1/agents/", json=agent_data, headers=logged_in_headers)
    agent_id = create_response.json()["id"]

    # Delete the agent
    response = await client.delete(f"api/v1/agents/{agent_id}", headers=logged_in_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's gone
    get_response = await client.get(f"api/v1/agents/{agent_id}", headers=logged_in_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


async def test_read_agent_not_found(client: AsyncClient, logged_in_headers):
    response = await client.get("api/v1/agents/00000000-0000-0000-0000-000000000000", headers=logged_in_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
