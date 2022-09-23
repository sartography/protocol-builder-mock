"""'Open to Enrollment' replacement

Revision ID: 2a10c0990574
Revises: 0659a655b5be
Create Date: 2022-09-19 10:19:24.269914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a10c0990574'
down_revision = '0659a655b5be'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE irb_info_status SET \"STATUS\" = 'Open to Enrollment' WHERE \"STATUS\" like 'Open to enrollment'")


def downgrade():
    op.execute("UPDATE irb_info_status SET \"STATUS\" = 'Open to enrollment' WHERE \"STATUS\" like 'Open to Enrollment'")
