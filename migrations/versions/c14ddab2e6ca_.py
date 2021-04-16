"""empty message

Revision ID: c14ddab2e6ca
Revises: 277f05065db0
Create Date: 2021-04-16 16:14:16.854779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c14ddab2e6ca'
down_revision = '277f05065db0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('irb_info', 'RB_OF_RECORD')
    op.add_column('irb_info', sa.Column('IRB_OF_RECORD', sa.String(), default=''))


def downgrade():
    op.drop_column('irb_info', 'IRB_OF_RECORD')
    op.add_column('irb_info', sa.Column('RB_OF_RECORD', sa.String(), default=''))
