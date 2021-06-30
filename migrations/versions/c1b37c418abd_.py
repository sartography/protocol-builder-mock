""" add irb_info_event and irb_info_status tables

Revision ID: c1b37c418abd
Revises: 6c34576847ab
Create Date: 2021-06-17 12:40:05.411279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1b37c418abd'
down_revision = 'af3a7d80c102'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('irb_info', 'IRBEVENT')
    op.create_table('irb_info_event',
    sa.Column('STUDY_ID', sa.Integer(), nullable=False),
    sa.Column('EVENT_ID', sa.String(), nullable=False, default=''),
    sa.Column('EVENT', sa.String(), nullable=False, default=''),
    sa.ForeignKeyConstraint(['STUDY_ID'], ['irb_info.SS_STUDY_ID'], ),
    sa.PrimaryKeyConstraint('STUDY_ID'))

    op.drop_column('irb_info', 'IRB_STATUS')
    op.create_table('irb_info_status',
    sa.Column('STUDY_ID', sa.Integer(), nullable=False),
    sa.Column('STATUS_ID', sa.String(), nullable=False),
    sa.Column('STATUS', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(('STUDY_ID',), ['irb_info.SS_STUDY_ID'], ),
    sa.PrimaryKeyConstraint('STUDY_ID'))


def downgrade():
    op.drop_table('irb_info_event')
    op.add_column('irb_info', sa.Column('IRBEVENT', sa.String(), nullable=True, default=''))
    op.drop_table('irb_info_status')
    op.add_column('irb_info', sa.Column('IRB_STATUS', sa.String(), nullable=True, default=''))
