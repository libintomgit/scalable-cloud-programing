"""add apt_num to address table

Revision ID: f6cc6fe60dd5
Revises: 
Create Date: 2023-03-14 16:53:01.522775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6cc6fe60dd5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))




def downgrade():
    op.drop_colum('address', 'apt_num')
