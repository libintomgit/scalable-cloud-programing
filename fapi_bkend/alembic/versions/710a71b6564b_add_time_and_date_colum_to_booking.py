"""add time and date colum to booking

Revision ID: 710a71b6564b
Revises: 5d13c3731535
Create Date: 2023-03-19 16:58:05.107146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '710a71b6564b'
down_revision = '5d13c3731535'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('booking', sa.Column('date', sa.String(), nullable=False))
    op.add_column('booking', sa.Column('time', sa.String(), nullable=False))



def downgrade():
    op.drop_column('date')
    op.drop_column('time')
