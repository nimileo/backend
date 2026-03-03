"""add auth tables

Revision ID: 1bb6136bf1ae
Revises: 
Create Date: 2026-03-02 15:35:56.816964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bb6136bf1ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'otp_verifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('otp_hash', sa.String(255), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('attempts', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime()),
    )

def downgrade():
    op.drop_table('otp_verifications')
