"""add foreign key to posts for users

Revision ID: 22f85cbaad11
Revises: a434c67fd6a2
Create Date: 2023-06-01 15:36:24.518403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22f85cbaad11'
down_revision = 'a434c67fd6a2'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('posts', sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
