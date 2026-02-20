import asyncio
import uuid

from fastapi import status
from langflow.services.deps import get_queue_service


async def test_get_a2a_agent_card(client, logged_in_headers):
    response = await client.get("api/v1/a2a/agent-card", headers=logged_in_headers)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["protocol"] == "a2a"
    assert "task.create" in result["capabilities"]


async def test_create_a2a_task(client, logged_in_headers, flow, monkeypatch):
    async def mock_start_flow_build(**_kwargs):
        return "task-123"

    import langflow.api.v1.a2a

    monkeypatch.setattr(langflow.api.v1.a2a, "start_flow_build", mock_start_flow_build)

    response = await client.post("api/v1/a2a/tasks", json={"flow_id": str(flow.id)}, headers=logged_in_headers)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["id"] == "task-123"
    assert result["status"] == "submitted"


async def test_get_a2a_task_status_running(client, logged_in_headers):
    hold_event = asyncio.Event()

    async def hold_task():
        await hold_event.wait()

    queue_service = get_queue_service()
    task_id = str(uuid.uuid4())
    queue_service.create_queue(task_id)
    queue_service.start_job(task_id, hold_task())

    try:
        response = await client.get(f"api/v1/a2a/tasks/{task_id}", headers=logged_in_headers)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result["status"] == "running"
        assert result["done"] is False
    finally:
        hold_event.set()
        await queue_service.cleanup_job(task_id)


async def test_cancel_a2a_task(client, logged_in_headers):
    hold_event = asyncio.Event()

    async def hold_task():
        await hold_event.wait()

    queue_service = get_queue_service()
    task_id = str(uuid.uuid4())
    queue_service.create_queue(task_id)
    queue_service.start_job(task_id, hold_task())

    try:
        response = await client.post(f"api/v1/a2a/tasks/{task_id}/cancel", headers=logged_in_headers)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result["success"] is True
    finally:
        hold_event.set()
        await queue_service.cleanup_job(task_id)
