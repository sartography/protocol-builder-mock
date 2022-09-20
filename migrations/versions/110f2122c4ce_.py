"""empty message

Revision ID: 110f2122c4ce
Revises: 0659a655b5be
Create Date: 2022-09-14 12:09:19.355174

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision = '110f2122c4ce'
down_revision = '0659a655b5be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('study', sa.Column('DATE_CREATED', sa.Date(), nullable=True, server_default=func.now()))


def downgrade():
    op.drop_column('study', 'DATE_CREATED')
