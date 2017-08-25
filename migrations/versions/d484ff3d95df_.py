"""empty message

Revision ID: d484ff3d95df
Revises: 95567bad80b7
Create Date: 2017-08-25 13:36:38.012000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd484ff3d95df'
down_revision = '95567bad80b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('browser', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('ip', sa.Integer(), nullable=True))
    op.add_column('comments', sa.Column('language', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('location', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('network', sa.String(length=64), nullable=True))
    op.add_column('comments', sa.Column('os', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'os')
    op.drop_column('comments', 'network')
    op.drop_column('comments', 'location')
    op.drop_column('comments', 'language')
    op.drop_column('comments', 'ip')
    op.drop_column('comments', 'browser')
    # ### end Alembic commands ###
