"""empty message

Revision ID: 277f05065db0
Revises: 119c1269ee7c
Create Date: 2021-04-07 16:14:01.470659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '277f05065db0'
down_revision = '119c1269ee7c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('irb_info',
    sa.Column('SS_STUDY_ID', sa.Integer(), nullable=False),
    sa.Column('UVA_STUDY_TRACKING', sa.String(), nullable=False, default=''),
    sa.Column('DATE_MODIFIED', sa.DateTime(timezone=True), nullable=True),
    sa.Column('IRB_ADMINISTRATIVE_REVIEWER', sa.String(), nullable=False, default=''),
    sa.Column('AGENDA_DATE', sa.DateTime(timezone=True), nullable=True),
    sa.Column('IRB_REVIEW_TYPE', sa.String(), nullable=False, default=''),
    sa.Column('IRBEVENT', sa.String(), nullable=False, default=''),
    sa.Column('IRB_STATUS', sa.String(), nullable=False, default=''),
    sa.Column('RB_OF_RECORD', sa.String(), nullable=False, default=''),
    sa.Column('UVA_IRB_HSR_IS_IRB_OF_RECORD_FOR_ALL_SITES', sa.Integer(), nullable=True),
    sa.Column('STUDYIRBREVIEWERADMIN', sa.String(), nullable=False, default=''),
    sa.ForeignKeyConstraint(['SS_STUDY_ID'], ['study.STUDYID'],),
    sa.PrimaryKeyConstraint('SS_STUDY_ID'))


def downgrade():
    op.drop_table('irb_info')
