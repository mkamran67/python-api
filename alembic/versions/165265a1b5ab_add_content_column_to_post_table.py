"""Add content column to post table

Revision ID: 165265a1b5ab
Revises: aab37bb2fd8a
Create Date: 2022-03-23 22:30:37.101667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '165265a1b5ab'
down_revision = 'aab37bb2fd8a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts')
