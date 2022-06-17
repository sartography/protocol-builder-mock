"""add pre_review table

Revision ID: 0659a655b5be
Revises: fcc193c49110
Create Date: 2022-06-16 10:03:33.853014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0659a655b5be'
down_revision = 'fcc193c49110'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pre_review',
        sa.Column('PROT_EVENT_ID', sa.Integer()),
        sa.Column('SS_STUDY_ID', sa.Integer(), nullable=False),
        sa.Column('DATEENTERED', sa.DateTime(timezone=True)),
        sa.Column('REVIEW_TYPE', sa.Integer()),
        sa.Column('COMMENTS', sa.String(), nullable=False, default=''),
        sa.Column('IRBREVIEWERADMIN', sa.String()),
        sa.Column('FNAME', sa.String()),
        sa.Column('LNAME', sa.String()),
        sa.Column('LOGIN', sa.String(), nullable=False, default=''),
        sa.Column('EVENT_TYPE', sa.Integer()),
        sa.Column('STATUS', sa.String()),
        sa.Column('DETAIL', sa.String()),
        sa.ForeignKeyConstraint(['SS_STUDY_ID'], ['study.STUDYID'], ),
        sa.PrimaryKeyConstraint('PROT_EVENT_ID')
    )


def downgrade():
    op.drop_table('pre_review')
