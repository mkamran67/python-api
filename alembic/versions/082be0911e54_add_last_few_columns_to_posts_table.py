"""Add last few columns to posts table

Revision ID: 082be0911e54
Revises: be22ea5a9e66
Create Date: 2022-03-24 20:00:12.234207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082be0911e54'
down_revision = 'be22ea5a9e66'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass

def downgrade():
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
