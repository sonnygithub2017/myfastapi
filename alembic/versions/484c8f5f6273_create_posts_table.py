"""create posts table

Revision ID: 484c8f5f6273
Revises: 
Create Date: 2023-06-01 13:56:45.585623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '484c8f5f6273'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_table('posts')
