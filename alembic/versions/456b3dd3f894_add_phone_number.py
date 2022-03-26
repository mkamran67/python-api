"""Add phone number

Revision ID: 456b3dd3f894
Revises: 70b93912cd60
Create Date: 2022-03-26 11:41:19.161297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '456b3dd3f894'
down_revision = '70b93912cd60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
