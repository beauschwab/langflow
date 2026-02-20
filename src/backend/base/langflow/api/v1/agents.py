from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlmodel import col, select

from langflow.api.utils import CurrentActiveUser, DbSession
from langflow.logging import logger
from langflow.services.database.models.agent.model import Agent, AgentCreate, AgentRead, AgentUpdate

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/", response_model=AgentRead, status_code=201)
async def create_agent(
    *,
    session: DbSession,
    agent: AgentCreate,
    current_user: CurrentActiveUser,
):
    """Create a new agent."""
    try:
        if agent.user_id is None:
            agent.user_id = current_user.id

        db_agent = Agent.model_validate(agent, from_attributes=True)
        session.add(db_agent)
        await session.commit()
        await session.refresh(db_agent)
        return db_agent
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="Agent name must be unique") from e
        if hasattr(e, "errors"):
            raise HTTPException(status_code=400, detail="Invalid agent data") from e
        if isinstance(e, HTTPException):
            raise
        logger.exception("Error creating agent")
        raise HTTPException(status_code=500, detail="An internal error occurred while creating the agent") from e


@router.get("/", response_model=list[AgentRead])
async def read_agents(
    *,
    session: DbSession,
    current_user: CurrentActiveUser,
    search: str | None = None,
    agent_type: str | None = None,
):
    """List agents for the current user."""
    try:
        stmt = select(Agent).where(Agent.user_id == current_user.id)
        if search:
            stmt = stmt.where(col(Agent.name).ilike(f"%{search}%"))
        if agent_type:
            stmt = stmt.where(Agent.agent_type == agent_type)
        stmt = stmt.order_by(Agent.updated_at.desc())  # type: ignore[union-attr]
        agents = (await session.exec(stmt)).all()
        return agents
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        logger.exception("Error reading agents")
        raise HTTPException(status_code=500, detail="An internal error occurred while listing agents") from e


@router.get("/{agent_id}", response_model=AgentRead)
async def read_agent(
    *,
    session: DbSession,
    agent_id: UUID,
    current_user: CurrentActiveUser,
):
    """Get a specific agent by ID."""
    agent = await session.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return agent


@router.patch("/{agent_id}", response_model=AgentRead)
async def update_agent(
    *,
    session: DbSession,
    agent_id: UUID,
    agent: AgentUpdate,
    current_user: CurrentActiveUser,
):
    """Update an existing agent."""
    db_agent = await session.get(Agent, agent_id)
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if db_agent.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    agent_data = agent.model_dump(exclude_unset=True)
    for key, value in agent_data.items():
        setattr(db_agent, key, value)
    db_agent.updated_at = datetime.now(timezone.utc)

    session.add(db_agent)
    await session.commit()
    await session.refresh(db_agent)
    return db_agent


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(
    *,
    session: DbSession,
    agent_id: UUID,
    current_user: CurrentActiveUser,
):
    """Delete an agent."""
    db_agent = await session.get(Agent, agent_id)
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if db_agent.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    await session.delete(db_agent)
    await session.commit()
