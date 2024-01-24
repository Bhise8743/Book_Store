"""init added is_super_user column

Revision ID: 071e5322fef6
Revises: 203bb514ee6d
Create Date: 2024-01-23 16:59:59.771614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '071e5322fef6'
down_revision: Union[str, None] = '203bb514ee6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_super_user', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_super_user')
    # ### end Alembic commands ###
