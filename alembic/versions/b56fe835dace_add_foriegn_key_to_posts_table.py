"""add foriegn key to posts table

Revision ID: b56fe835dace
Revises: 9c88e30c1bba
Create Date: 2024-03-27 13:42:59.591404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b56fe835dace'
down_revision: Union[str, None] = '9c88e30c1bba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
