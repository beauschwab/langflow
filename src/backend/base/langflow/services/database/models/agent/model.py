from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from pydantic import field_serializer, field_validator
from sqlalchemy import Text, UniqueConstraint
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from langflow.services.database.models.flow import Flow
    from langflow.services.database.models.user import User


class AgentBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = Field(default=None, sa_column=Column(Text, index=True, nullable=True))
    agent_type: str | None = Field(default=None, nullable=True, description="Agent type identifier")
    config: dict | None = Field(default=None, sa_column=Column(JSON))
    tools: list[str] | None = Field(default=None, sa_column=Column(JSON))
    tags: list[str] | None = None
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True)

    @field_serializer("updated_at")
    def serialize_datetime(self, value):
        if isinstance(value, datetime):
            value = value.replace(microsecond=0)
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return value.isoformat()
        return value

    @field_validator("updated_at", mode="before")
    @classmethod
    def validate_dt(cls, v):
        if v is None:
            return v
        if isinstance(v, datetime):
            return v
        return datetime.fromisoformat(v)

    @field_validator("config")
    @classmethod
    def validate_config(cls, v):
        if v is not None and not isinstance(v, dict):
            msg = "Agent config must be a valid JSON object"
            raise ValueError(msg)
        return v


class Agent(AgentBase, table=True):  # type: ignore[call-arg]
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    config: dict | None = Field(default=None, sa_column=Column(JSON))
    tools: list[str] | None = Field(default=None, sa_column=Column(JSON))
    tags: list[str] | None = Field(sa_column=Column(JSON), default=[])
    user_id: UUID | None = Field(index=True, foreign_key="user.id", nullable=True)
    user: "User" = Relationship(back_populates="agents")
    flow_id: UUID | None = Field(default=None, foreign_key="flow.id", nullable=True, index=True)
    flow: Optional["Flow"] = Relationship(back_populates="agents")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint("user_id", "name", name="unique_agent_name"),)


class AgentCreate(AgentBase):
    user_id: UUID | None = None
    flow_id: UUID | None = None


class AgentRead(AgentBase):
    id: UUID
    user_id: UUID | None = Field()
    flow_id: UUID | None = Field()
    tags: list[str] | None = Field(None)
    created_at: datetime | None = None


class AgentUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    agent_type: str | None = None
    config: dict | None = None
    tools: list[str] | None = None
    tags: list[str] | None = None
    flow_id: UUID | None = None
