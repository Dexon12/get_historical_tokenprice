"""Initial revision

Revision ID: 3782343804b0
Revises: 
Create Date: 2025-01-10 02:11:18.832440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3782343804b0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'price_history',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('token_in', sa.String(length=255), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('network', sa.Enum('ethereum', name='networkslug'), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('round_id', sa.Integer(), nullable=False),
        sa.UniqueConstraint('token', 'token_in', 'network', 'timestamp', name='uq_token_price_history')
    )

    op.create_index('ix_price_history_token', 'price_history', ['token'], unique=False)
    op.create_index('ix_price_history_token_in', 'price_history', ['token_in'], unique=False)
    op.create_index('ix_price_history_timestamp', 'price_history', ['timestamp'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_price_history_timestamp', table_name='price_history')
    op.drop_index('ix_price_history_token_in', table_name='price_history')
    op.drop_index('ix_price_history_token', table_name='price_history')

    op.drop_table('price_history')

    network_slug_enum = postgresql.ENUM(
        'ethereum',
        name='networkslug'
    )
    network_slug_enum.drop(op.get_bind())
