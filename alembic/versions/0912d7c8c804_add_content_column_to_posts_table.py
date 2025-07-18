"""add content column to posts table

Revision ID: 0912d7c8c804
Revises: b699c8437787
Create Date: 2025-07-15 19:51:20.738977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0912d7c8c804'
down_revision: Union[str, Sequence[str], None] = 'b699c8437787'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
