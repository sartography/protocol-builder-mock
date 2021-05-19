"""add required_documents_list table

Revision ID: 5211917b2061
Revises: 6c34576847ab
Create Date: 2021-05-18 12:17:32.345927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5211917b2061'
down_revision = '6c34576847ab'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('required_documents_list',
    sa.Column('AUXDOCID', sa.String(), nullable=False),
    sa.Column('AUXDOC', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('AUXDOCID')
    )


def downgrade():
    op.drop_table('required_documents_list')
