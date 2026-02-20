from __future__ import annotations

import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from langflow.api.build import cancel_flow_build, get_flow_events_response, start_flow_build
from langflow.api.limited_background_tasks import LimitVertexBuildBackgroundTasks
from langflow.api.utils import CurrentActiveUser
from langflow.api.v1.schemas import (
    A2AAgentCardResponse,
    A2ATaskCreateRequest,
    A2ATaskResponse,
    A2ATaskStatusResponse,
    CancelFlowResponse,
)
from langflow.services.database.models.flow import Flow
from langflow.services.deps import get_queue_service, get_settings_service, session_scope
from langflow.services.job_queue.service import JobQueueService

router = APIRouter(prefix="/a2a", tags=["A2A"])


def _check_a2a_enabled() -> None:
    if not get_settings_service().settings.a2a_enabled:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A2A endpoints are disabled")


@router.get("/agent-card", response_model=A2AAgentCardResponse)
async def get_agent_card(current_user: CurrentActiveUser) -> A2AAgentCardResponse:  # noqa: ARG001
    _check_a2a_enabled()
    settings = get_settings_service().settings
    return A2AAgentCardResponse(
        capabilities=["task.create", "task.get", "task.cancel", "task.events.stream"],
        auth_schemes=["bearer"],
        orchestrator_backend=settings.orchestrator_backend,
    )


@router.post("/tasks", response_model=A2ATaskResponse)
async def create_task(
    *,
    request: A2ATaskCreateRequest,
    background_tasks: LimitVertexBuildBackgroundTasks,
    current_user: CurrentActiveUser,
    queue_service: Annotated[JobQueueService, Depends(get_queue_service)],
) -> A2ATaskResponse:
    _check_a2a_enabled()
    async with session_scope() as session:
        flow = await session.get(Flow, request.flow_id)
        if not flow:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flow not found: {request.flow_id}")

    task_id = await start_flow_build(
        flow_id=request.flow_id,
        background_tasks=background_tasks,
        inputs=request.inputs,
        data=request.data,
        files=request.files,
        stop_component_id=request.stop_component_id,
        start_component_id=request.start_component_id,
        log_builds=request.log_builds,
        current_user=current_user,
        queue_service=queue_service,
        flow_name=request.flow_name,
    )
    return A2ATaskResponse(
        id=task_id,
        status="submitted",
        status_url=f"/api/v1/a2a/tasks/{task_id}",
        events_url=f"/api/v1/a2a/tasks/{task_id}/events",
        cancel_url=f"/api/v1/a2a/tasks/{task_id}/cancel",
    )


@router.get("/tasks/{task_id}", response_model=A2ATaskStatusResponse)
async def get_task_status(
    task_id: str,
    current_user: CurrentActiveUser,  # noqa: ARG001
    queue_service: Annotated[JobQueueService, Depends(get_queue_service)],
) -> A2ATaskStatusResponse:
    _check_a2a_enabled()
    try:
        _, _, event_task = queue_service.get_queue_data(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if event_task is None:
        return A2ATaskStatusResponse(id=task_id, status="submitted", done=False)
    if event_task.cancelled():
        return A2ATaskStatusResponse(id=task_id, status="cancelled", done=True)
    if event_task.done():
        try:
            error = event_task.exception()
        except asyncio.InvalidStateError:
            logger.error(f"Inconsistent task state detected for task_id {task_id}")
            return A2ATaskStatusResponse(id=task_id, status="failed", done=True, error="Inconsistent task state")
        if error is not None:
            return A2ATaskStatusResponse(id=task_id, status="failed", done=True, error=str(error))
        return A2ATaskStatusResponse(id=task_id, status="completed", done=True)

    return A2ATaskStatusResponse(id=task_id, status="running", done=False)


@router.get("/tasks/{task_id}/events")
async def get_task_events(
    task_id: str,
    current_user: CurrentActiveUser,  # noqa: ARG001
    queue_service: Annotated[JobQueueService, Depends(get_queue_service)],
    *,
    stream: bool = True,
):
    _check_a2a_enabled()
    return await get_flow_events_response(job_id=task_id, queue_service=queue_service, stream=stream)


@router.post("/tasks/{task_id}/cancel", response_model=CancelFlowResponse)
async def cancel_task(
    task_id: str,
    current_user: CurrentActiveUser,  # noqa: ARG001
    queue_service: Annotated[JobQueueService, Depends(get_queue_service)],
) -> CancelFlowResponse:
    _check_a2a_enabled()
    try:
        cancellation_success = await cancel_flow_build(job_id=task_id, queue_service=queue_service)
        if cancellation_success:
            return CancelFlowResponse(success=True, message="Task cancelled successfully")
        return CancelFlowResponse(success=False, message="Failed to cancel task")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception(f"Error cancelling A2A task for task_id {task_id}: {exc}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
