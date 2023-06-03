"""create users table

Revision ID: a434c67fd6a2
Revises: 13880b76142d
Create Date: 2023-06-01 15:09:54.088909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a434c67fd6a2'
down_revision = '13880b76142d'
branch_labels = None
depends_on = None

def upgrade() -> None:
  op.create_table(
    'users', sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('create_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
  )

def downgrade() -> None:
    op.drop_table('users')
