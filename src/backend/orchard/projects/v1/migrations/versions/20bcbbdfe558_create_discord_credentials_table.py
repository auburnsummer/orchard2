"""create discord credentials table

Revision ID: 20bcbbdfe558
Revises: 4e8c5d00f5f9
Create Date: 2023-06-30 05:12:46.853307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20bcbbdfe558'
down_revision = '4e8c5d00f5f9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "discord_credentials", 
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id"))
    )

def downgrade() -> None:
    op.drop_table("discord_credentials")
