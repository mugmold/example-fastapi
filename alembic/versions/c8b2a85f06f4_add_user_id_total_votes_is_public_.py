"""add user_id,total_votes,is_public,created_at to posts table

Revision ID: c8b2a85f06f4
Revises: dc1b2fcaee88
Create Date: 2025-07-15 20:20:19.768407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8b2a85f06f4'
down_revision: Union[str, Sequence[str], None] = 'dc1b2fcaee88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), sa.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False))
    op.add_column('posts', sa.Column('total_votes', sa.Integer(),
                                     nullable=False, default=0))
    op.add_column('posts', sa.Column('is_public', sa.Boolean(),
                                     nullable=False, server_default=sa.text('true')))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(timezone=True),
                                     server_default=sa.func.now(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'user_id'),
    op.drop_column('posts', 'total_votes'),
    op.drop_column('posts', 'is_public'),
    op.drop_column('posts', 'created_at')
    pass
