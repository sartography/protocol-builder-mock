"""empty message

Revision ID: 6c34576847ab
Revises: c14ddab2e6ca
Create Date: 2021-05-11 11:10:14.725089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c34576847ab'
down_revision = 'c14ddab2e6ca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('selected_user',
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('selected_user', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )


def downgrade():
    op.drop_table('selected_user')
