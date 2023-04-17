"""adding missing address_id column in the restaurants table

Revision ID: 418f026bf8d1
Revises: 62add35d383c
Create Date: 2023-03-19 14:36:27.306931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '418f026bf8d1'
down_revision = '62add35d383c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('restaurants', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_restaurants_fk', source_table="restaurants", referent_table="address",
                          local_cols=['address_id'], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    pass
