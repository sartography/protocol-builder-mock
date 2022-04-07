"""Add 'IRB_ONLINE_STATUS' column to IRBInfo table

Revision ID: fcc193c49110
Revises: d6627c76ed75
Create Date: 2022-04-07 16:00:36.260246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcc193c49110'
down_revision = 'd6627c76ed75'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('irb_info', sa.Column('IRB_ONLINE_STATUS', sa.String(), nullable=True))


def downgrade():
    op.drop_column('irb_info', 'IRB_ONLINE_STATUS')
