"""add new study detail

Revision ID: af3a7d80c102
Revises: 6c34576847ab
Create Date: 2021-05-26 16:24:37.196893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af3a7d80c102'
down_revision = '6c34576847ab'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('study_details', sa.Column('UVA_STUDY_TRACKING', sa.String(), nullable=True))


def downgrade():
    op.drop_column('study_details', 'UVA_STUDY_TRACKING')
