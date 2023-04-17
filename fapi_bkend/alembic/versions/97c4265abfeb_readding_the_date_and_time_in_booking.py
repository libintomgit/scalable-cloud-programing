"""readding the date and time in booking

Revision ID: 97c4265abfeb
Revises: 710a71b6564b
Create Date: 2023-03-20 16:47:30.545144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c4265abfeb'
down_revision = '710a71b6564b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('booking', sa.Column('booking_date', sa.String(), nullable=True))
    op.add_column('booking', sa.Column('booking_time', sa.String(), nullable=True))



def downgrade():
    op.drop_column('booking', 'date')
    op.drop_column('booking', 'time')
