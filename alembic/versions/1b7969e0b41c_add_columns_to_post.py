"""add columns to post

Revision ID: 1b7969e0b41c
Revises: b56fe835dace
Create Date: 2024-03-27 13:48:33.695281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b7969e0b41c'
down_revision: Union[str, None] = 'b56fe835dace'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    

def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
