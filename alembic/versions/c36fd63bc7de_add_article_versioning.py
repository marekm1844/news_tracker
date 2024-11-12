"""Add article versioning

Revision ID: c36fd63bc7de
Revises: 0b1e33338644
Create Date: 2024-11-12 17:41:12.508129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c36fd63bc7de'
down_revision: Union[str, None] = '0b1e33338644'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'title')
    op.drop_column('articles', 'content')
    op.drop_column('articles', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.add_column('articles', sa.Column('content', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('articles', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
