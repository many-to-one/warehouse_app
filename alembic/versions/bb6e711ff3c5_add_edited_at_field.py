"""add edited_at field

Revision ID: bb6e711ff3c5
Revises: 5d6aba9657d5
Create Date: 2024-08-05 07:41:58.931257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb6e711ff3c5'
down_revision: Union[str, None] = '5d6aba9657d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products_list', sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.add_column('products_list', sa.Column('edited_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.add_column('token_blacklist', sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    op.add_column('users', sa.Column('edited_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'edited_at')
    op.drop_column('token_blacklist', 'created_at')
    op.drop_column('products_list', 'edited_at')
    op.drop_column('products_list', 'created_at')
    # ### end Alembic commands ###
