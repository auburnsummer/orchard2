"""Create users table

Revision ID: 4e8c5d00f5f9
Revises: 
Create Date: 2023-06-21 05:27:05.604008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e8c5d00f5f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users", 
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("name", sa.String)
    )


def downgrade() -> None:
    op.drop_table("users")
