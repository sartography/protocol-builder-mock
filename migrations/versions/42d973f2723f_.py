"""Drop HSRNUMBER column from study table

Revision ID: 42d973f2723f
Revises: c1b37c418abd
Create Date: 2021-08-16 09:37:36.766180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42d973f2723f'
down_revision = 'c1b37c418abd'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('study', 'HSRNUMBER')


def downgrade():
    op.add_column('study', sa.Column('HSRNUMBER', sa.String(), nullable=True))
