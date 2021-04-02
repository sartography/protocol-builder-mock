"""empty message

Revision ID: 93a1e2ce38dc
Revises: 6cd52db404f6
Create Date: 2021-03-29 15:06:32.100287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a1e2ce38dc'
down_revision = '6cd52db404f6'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('study_details', 'DSMB')
    op.add_column('study_details', sa.Column('DSMB', sa.VARCHAR, nullable=True))
    op.add_column('study_details', sa.Column('REVIEW_TYPE', sa.Integer, nullable=True))
    op.add_column('study_details', sa.Column('REVIEWTYPENAME', sa.VARCHAR, nullable=True))


def downgrade():
    op.drop_column('study_details', 'DSMB')
    op.add_column('study_details', sa.Column('DSMB', sa.Integer, nullable=True))
    op.drop_column('study_details', 'REVIEW_TYPE')
    op.drop_column('study_details', 'REVIEWTYPENAME')
