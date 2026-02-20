from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Column, DateTime, Field, SQLModel, UniqueConstraint, func

class TenantMembershipRole(str, Enum):
    """Role levels for tenant membership, from owner-level administration to read-only access."""

    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"


class Tenant(SQLModel, table=True):  # type: ignore[call-arg]
    """Tenant workspace metadata used to partition enterprise users and resources."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    name: str = Field(index=True, unique=True)
    slug: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )


class TenantMembership(SQLModel, table=True):  # type: ignore[call-arg]
    """Association table linking users to tenants with an access role and activation state."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    tenant_id: UUID = Field(foreign_key="tenant.id", index=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    role: TenantMembershipRole = Field(default=TenantMembershipRole.MEMBER)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    __table_args__ = (UniqueConstraint("tenant_id", "user_id", name="unique_tenant_membership"),)
