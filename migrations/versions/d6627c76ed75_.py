"""empty message

Revision ID: d6627c76ed75
Revises: 42d973f2723f
Create Date: 2021-11-08 13:53:51.020066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6627c76ed75'
down_revision = '42d973f2723f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE required_document RENAME COLUMN "AUXDOC" TO "AUXILIARY_DOC"')
    op.execute('ALTER TABLE required_document RENAME COLUMN "AUXDOCID" TO "SS_AUXILIARY_DOC_TYPE_ID"')


def downgrade():
    op.execute('ALTER TABLE required_document RENAME COLUMN "AUXILIARY_DOC" TO "AUXDOC"')
    op.execute('ALTER TABLE required_document RENAME COLUMN "SS_AUXILIARY_DOC_TYPE_ID" TO "AUXDOCID"')
