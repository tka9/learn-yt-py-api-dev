"""Add Content column to post table

Revision ID: ea05a8358b44
Revises: f372ccb5d02a
Create Date: 2024-03-27 13:32:02.550914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea05a8358b44'
down_revision: Union[str, None] = 'f372ccb5d02a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
