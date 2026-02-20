from contextlib import asynccontextmanager

import pytest
from langflow.api.v1 import mcp
from langflow.services.database.models.flow.model import Flow
from langflow.services.database.models.user.model import User


class _DBService:
    def __init__(self, session):
        self._session = session

    @asynccontextmanager
    async def with_session(self):
        yield self._session


class _StorageService:
    async def list_files(self, flow_id):  # noqa: ARG002
        return ["report.csv"]

    async def get_file(self, flow_id, file_name):  # noqa: ARG002
        return b"content"


class _SettingsService:
    class _Settings:
        holst = "localhost"
        port = 7860

    settings = _Settings()


async def _create_user_with_flow(async_session, *, username: str, flow_name: str):
    user = User(username=username, password="password", is_active=True)
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    flow = Flow(name=flow_name, user_id=user.id)
    async_session.add(flow)
    await async_session.commit()
    await async_session.refresh(flow)
    return user, flow


async def test_mcp_list_tools_scopes_to_current_user(async_session, monkeypatch):
    current_user, current_user_flow = await _create_user_with_flow(
        async_session, username="mcp-current-user", flow_name="current-user-flow"
    )
    await _create_user_with_flow(async_session, username="mcp-other-user", flow_name="other-user-flow")

    monkeypatch.setattr(mcp, "get_db_service", lambda: _DBService(async_session))
    monkeypatch.setattr(mcp, "json_schema_from_flow", lambda flow: {"title": flow.name})

    token = mcp.current_user_ctx.set(current_user)
    try:
        tools = await mcp.handle_list_tools()
    finally:
        mcp.current_user_ctx.reset(token)

    assert len(tools) == 1
    assert tools[0].name == current_user_flow.name


async def test_mcp_read_resource_rejects_cross_user_flow_access(async_session, monkeypatch):
    _owner_user, owner_flow = await _create_user_with_flow(async_session, username="mcp-owner", flow_name="owner-flow")
    other_user, _ = await _create_user_with_flow(async_session, username="mcp-other", flow_name="other-flow")

    monkeypatch.setattr(mcp, "get_db_service", lambda: _DBService(async_session))
    monkeypatch.setattr(mcp, "get_storage_service", lambda: _StorageService())
    monkeypatch.setattr(mcp, "get_settings_service", lambda: _SettingsService())

    token = mcp.current_user_ctx.set(other_user)
    try:
        with pytest.raises(ValueError):
            await mcp.handle_read_resource(f"http://localhost:7860/api/v1/files/{owner_flow.id}/report.csv")
    finally:
        mcp.current_user_ctx.reset(token)
