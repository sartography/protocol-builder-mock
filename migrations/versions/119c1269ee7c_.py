"""empty message

Revision ID: 119c1269ee7c
Revises: 93a1e2ce38dc
Create Date: 2021-03-31 12:30:19.645458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '119c1269ee7c'
down_revision = '93a1e2ce38dc'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('study', 'Q_COMPLETE')
    op.create_table('irb_status',
    sa.Column('STUDYID', sa.Integer(), nullable=False),
    sa.Column('STATUS', sa.String(), nullable=False, default=''),
    sa.Column('DETAIL', sa.String(), nullable=False, default=''),
    sa.ForeignKeyConstraint(['STUDYID'], ['study.STUDYID'],),
    sa.PrimaryKeyConstraint('STUDYID')
    )



def downgrade():
    op.drop_table('irb_status')
    op.add_column('study', sa.Column('Q_COMPLETE', sa.Boolean(), nullable=True))
