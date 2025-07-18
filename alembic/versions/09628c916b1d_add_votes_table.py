"""add votes table

Revision ID: 09628c916b1d
Revises: c8b2a85f06f4
Create Date: 2025-07-15 20:37:00.838005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09628c916b1d'
down_revision: Union[str, Sequence[str], None] = 'c8b2a85f06f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey(
                        'users.id', ondelete='CASCADE'), primary_key=True),
                    sa.Column('post_id', sa.Integer(), sa.ForeignKey(
                        'posts.id', ondelete='CASCADE'), primary_key=True),
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('votes')
    pass
