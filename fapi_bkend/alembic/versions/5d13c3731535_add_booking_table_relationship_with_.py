"""add booking table relationship with restaurant

Revision ID: 5d13c3731535
Revises: 418f026bf8d1
Create Date: 2023-03-19 16:06:47.125576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d13c3731535'
down_revision = '418f026bf8d1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('booking',
                sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                sa.Column('name', sa.String(), nullable=False),
                sa.Column('location', sa.String(), nullable=False),
                sa.Column('email_id', sa.String(), nullable=False),
                sa.Column('phone_number', sa.String(), nullable=False),
                sa.Column('complete', sa.Boolean(), nullable=False),
                sa.Column('restr_id', sa.Integer(), nullable=False)
                )
    op.create_foreign_key('restr_booking_fk', source_table='booking', referent_table='restaurants',
                local_cols=['restr_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('restr_booking_fk', table_name="booking")
    op.drop_table('booking')
