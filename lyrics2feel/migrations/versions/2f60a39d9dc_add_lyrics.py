"""add lyrics

Revision ID: 2f60a39d9dc
Revises: 19b244e1b5
Create Date: 2014-09-03 01:10:52.811381

"""

# revision identifiers, used by Alembic.
revision = '2f60a39d9dc'
down_revision = '19b244e1b5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lyrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track', sa.Unicode(), nullable=False),
    sa.Column('album', sa.Unicode(), nullable=False),
    sa.Column('artist', sa.Unicode(), nullable=False),
    sa.Column('lyrics', sa.UnicodeText(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lyrics')
    ### end Alembic commands ###
