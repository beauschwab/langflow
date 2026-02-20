"""create agent table

Revision ID: a1b2c3d4e5f6
Revises: f3b2d1f1002d
Create Date: 2026-02-20 16:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from langflow.utils import migration

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "f3b2d1f1002d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    if not migration.table_exists("agent", conn):
        op.create_table(
            "agent",
            sa.Column("id", sa.CHAR(32), nullable=False),
            sa.Column("name", sa.VARCHAR(), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("agent_type", sa.VARCHAR(), nullable=True),
            sa.Column("config", sa.JSON(), nullable=True),
            sa.Column("tools", sa.JSON(), nullable=True),
            sa.Column("tags", sa.JSON(), nullable=True),
            sa.Column("user_id", sa.CHAR(32), nullable=True),
            sa.Column("flow_id", sa.CHAR(32), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
            sa.ForeignKeyConstraint(["flow_id"], ["flow.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "name", name="unique_agent_name"),
        )
        with op.batch_alter_table("agent", schema=None) as batch_op:
            batch_op.create_index("ix_agent_name", ["name"])
            batch_op.create_index("ix_agent_user_id", ["user_id"])
            batch_op.create_index("ix_agent_flow_id", ["flow_id"])


def downgrade() -> None:
    conn = op.get_bind()
    if migration.table_exists("agent", conn):
        op.drop_table("agent")
