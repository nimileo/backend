"""alter companies add auth fields

Revision ID: 6fea5f7ca0fa
Revises: 07bef20f283a
Create Date: 2026-03-02 15:47:41.618854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fea5f7ca0fa'
down_revision = '07bef20f283a'
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('companies',
        sa.Column('is_active', sa.Boolean(), nullable=True)
    )

    op.add_column('companies',
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

def downgrade():
    op.drop_column('companies', 'created_at')
    op.drop_column('companies', 'is_active')