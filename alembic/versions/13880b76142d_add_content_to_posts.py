"""add content to posts

Revision ID: 13880b76142d
Revises: 484c8f5f6273
Create Date: 2023-06-01 14:56:39.821012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13880b76142d'
down_revision = '484c8f5f6273'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content", sa.String()))

def downgrade() -> None:
    op.drop_column('posts', 'content')
