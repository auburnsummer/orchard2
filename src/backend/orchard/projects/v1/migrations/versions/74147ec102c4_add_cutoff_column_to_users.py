"""add cutoff column to users

Revision ID: 74147ec102c4
Revises: 20bcbbdfe558
Create Date: 2023-07-06 03:15:36.655783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74147ec102c4'
down_revision = '20bcbbdfe558'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('cutoff', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'cutoff')
    # ### end Alembic commands ###