"""first

Revision ID: bd4e2f88fed4
Revises: 
Create Date: 2022-09-29 00:02:02.233419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd4e2f88fed4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'User',
        sa.Column('ID', sa.String(10), primary_key=True),
        sa.Column('PassWd', sa.String(10)),
        sa.Column('Age', sa.Integer),
        sa.Column('Job', sa.Integer), # 직업의 유형별로 분류하여 숫자로 인코딩 할 예정
        sa.Column('Sex', sa.Integer)
    )


def downgrade():
    pass
