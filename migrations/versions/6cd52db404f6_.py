"""empty message

Revision ID: 6cd52db404f6
Revises: 9493f29b0898
Create Date: 2021-03-24 10:04:28.215143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cd52db404f6'
down_revision = '9493f29b0898'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('study_details', sa.Column('IS_SPONSOR_TRACKING', sa.Integer(), nullable=True))
    op.add_column('study_details', sa.Column('SPONSOR_TRACKING', sa.Integer(), nullable=True))
    op.add_column('study_details', sa.Column('IS_DSMB', sa.Integer(), nullable=True))
    op.add_column('study_details', sa.Column('IS_COMPLETE_NON_IRB_REGULATORY', sa.Integer(), nullable=True))
    op.add_column('study_details', sa.Column('IS_INSIDE_CONTRACT', sa.Integer(), nullable=True))
    op.add_column('study_details', sa.Column('IS_CODED_RESEARCH', sa.Integer(), nullable=True))
    op.add_column('study_details', sa.Column('IS_OUTSIDE_SPONSOR', sa.Integer(), nullable=True))
    op.add_column('study_details', sa.Column('IS_UVA_COLLABANALYSIS', sa.Integer(), nullable=True))
    op.drop_column('study_details', 'SPONSORS_PROTOCOL_REVISION_DATE')
    op.add_column('study_details', sa.Column('SPONSORS_PROTOCOL_REVISION_DATE', sa.Date(), nullable=True))


def downgrade():
    op.drop_column('study_details', 'IS_SPONSOR_TRACKING')
    op.drop_column('study_details', 'SPONSOR_TRACKING')
    op.drop_column('study_details', 'IS_DSMB')
    op.drop_column('study_details', 'IS_COMPLETE_NON_IRB_REGULATORY')
    op.drop_column('study_details', 'IS_INSIDE_CONTRACT')
    op.drop_column('study_details', 'IS_CODED_RESEARCH')
    op.drop_column('study_details', 'IS_OUTSIDE_SPONSOR')
    op.drop_column('study_details', 'IS_UVA_COLLABANALYSIS')
    op.drop_column('study_details', 'SPONSORS_PROTOCOL_REVISION_DATE')
    op.add_column('study_details', sa.Column('SPONSORS_PROTOCOL_REVISION_DATE', sa.Integer(), nullable=True))
