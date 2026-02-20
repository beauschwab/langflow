from sqlmodel import select

from langflow.services.database.models.tenant.model import Tenant, TenantMembership, TenantMembershipRole
from langflow.services.database.models.user.model import User


async def test_tenant_membership_defaults_to_member(async_session):
    user = User(username="tenant-member-user", password="testpassword", is_active=True, is_superuser=False)
    tenant = Tenant(name="Bank Finance", slug="bank-finance")
    async_session.add(user)
    async_session.add(tenant)
    await async_session.commit()
    await async_session.refresh(user)
    await async_session.refresh(tenant)

    membership = TenantMembership(tenant_id=tenant.id, user_id=user.id)
    async_session.add(membership)
    await async_session.commit()

    stored_membership = (
        await async_session.exec(
            select(TenantMembership).where(
                TenantMembership.tenant_id == tenant.id, TenantMembership.user_id == user.id
            )
        )
    ).first()

    assert stored_membership is not None
    assert stored_membership.role == TenantMembershipRole.MEMBER
