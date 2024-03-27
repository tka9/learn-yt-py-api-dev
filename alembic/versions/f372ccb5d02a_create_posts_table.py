"""Create Posts Table

Revision ID: f372ccb5d02a
Revises: 
Create Date: 2024-03-27 13:24:25.694145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f372ccb5d02a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('posts')
