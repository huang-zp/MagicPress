"""empty message

Revision ID: bb36e7fae8c0
Revises: d484ff3d95df
Create Date: 2017-08-26 16:02:02.711000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb36e7fae8c0'
down_revision = 'd484ff3d95df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('email', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('site', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('username', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'username')
    op.drop_column('comments', 'site')
    op.drop_column('comments', 'email')
    # ### end Alembic commands ###