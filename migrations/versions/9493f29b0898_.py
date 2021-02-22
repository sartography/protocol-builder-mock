"""empty message

Revision ID: 9493f29b0898
Revises: 34c57b2df4c6
Create Date: 2021-02-22 10:59:35.703414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9493f29b0898'
down_revision = '34c57b2df4c6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE study alter column "TITLE" TYPE text')


def downgrade():
    op.execute('ALTER TABLE study alter column "TITLE" TYPE varchar(80)')
