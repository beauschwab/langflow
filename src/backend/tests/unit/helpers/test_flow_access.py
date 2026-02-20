import pytest
from fastapi import HTTPException
from langflow.helpers.flow import get_flow_by_id_or_endpoint_name
from langflow.services.database.models.flow.model import Flow
from langflow.services.database.models.user.model import User


async def test_get_flow_by_id_enforces_user_ownership(async_session):
    owner = User(username="owner-user", password="password", is_active=True)
    other_user = User(username="other-user", password="password", is_active=True)
    async_session.add(owner)
    async_session.add(other_user)
    await async_session.commit()
    await async_session.refresh(owner)
    await async_session.refresh(other_user)

    flow = Flow(name="owner-flow", user_id=owner.id)
    async_session.add(flow)
    await async_session.commit()
    await async_session.refresh(flow)

    with pytest.raises(HTTPException) as exc:
        await get_flow_by_id_or_endpoint_name(str(flow.id), user_id=other_user.id)
    assert exc.value.status_code == 404

    flow_read = await get_flow_by_id_or_endpoint_name(str(flow.id), user_id=owner.id)
    assert flow_read is not None
    assert flow_read.id == flow.id
