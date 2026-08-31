"""create usage logs table

Revision ID: 544a3e8eeb06
Revises: 43751894f49d
Create Date: 2026-08-31 10:23:01.177038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '544a3e8eeb06'
down_revision: Union[str, Sequence[str], None] = '43751894f49d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'usage_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('api_key_id', sa.Integer(), nullable=False),
        sa.Column('endpoint', sa.String(), nullable=False),
        sa.Column('method', sa.String(), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=False),
        sa.Column('response_time', sa.Integer(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),
        sa.ForeignKeyConstraint(
            ['api_key_id'],
            ['api_keys.id']
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_usage_logs_id'),
        'usage_logs',
        ['id'],
        unique=False
    )

    op.create_index(
        op.f('ix_usage_logs_api_key_id'),
        'usage_logs',
        ['api_key_id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_usage_logs_api_key_id'),
        table_name='usage_logs'
    )

    op.drop_index(
        op.f('ix_usage_logs_id'),
        table_name='usage_logs'
    )

    op.drop_table('usage_logs')
