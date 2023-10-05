"""add content column to posts table

Revision ID: fa714a7cc293
Revises: e2e07b307b48
Create Date: 2023-10-04 15:48:58.127313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa714a7cc293'
down_revision: Union[str, None] = 'e2e07b307b48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
