"""add phone_no column to posts

Revision ID: 61b91b72b3ae
Revises: c4e51875a822
Create Date: 2023-10-05 10:14:19.467676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61b91b72b3ae'
down_revision: Union[str, None] = 'c4e51875a822'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Post', sa.Column('phone_number', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Post', 'phone_number')
    # ### end Alembic commands ###
