"""add user table

Revision ID: dc1b2fcaee88
Revises: 0912d7c8c804
Create Date: 2025-07-15 20:00:57.011833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc1b2fcaee88'
down_revision: Union[str, Sequence[str], None] = '0912d7c8c804'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(),
                              primary_key=True, nullable=False),
                    sa.Column('username', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.func.now(), nullable=False),
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
