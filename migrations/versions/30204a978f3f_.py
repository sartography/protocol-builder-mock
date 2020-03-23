"""empty message

Revision ID: 30204a978f3f
Revises: 
Create Date: 2020-02-17 13:48:46.974857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30204a978f3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('study',
    sa.Column('STUDYID', sa.Integer(), nullable=False),
    sa.Column('HSRNUMBER', sa.String(), nullable=True),
    sa.Column('TITLE', sa.String(length=80), nullable=False),
    sa.Column('NETBADGEID', sa.String(), nullable=False),
    sa.Column('Q_COMPLETE', sa.Boolean(), nullable=True),
    sa.Column('DATE_MODIFIED', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('STUDYID')
    )
    op.create_table('investigator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('STUDYID', sa.Integer(), nullable=True),
    sa.Column('NETBADGEID', sa.String(), nullable=False),
    sa.Column('INVESTIGATORTYPE', sa.String(), nullable=False),
    sa.Column('INVESTIGATORTYPEFULL', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['STUDYID'], ['study.STUDYID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('required_document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('AUXDOCID', sa.String(), nullable=False),
    sa.Column('AUXDOC', sa.String(), nullable=False),
    sa.Column('STUDYID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['STUDYID'], ['study.STUDYID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('required_document')
    op.drop_table('investigator')
    op.drop_table('study')
    # ### end Alembic commands ###