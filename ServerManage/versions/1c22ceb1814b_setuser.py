"""setUser

Revision ID: 1c22ceb1814b
Revises: d42b34f31023
Create Date: 2022-09-30 14:16:42.417590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c22ceb1814b'
down_revision = 'd42b34f31023'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('ID', sa.String(10), primary_key=True),
        sa.Column('PassWd', sa.String(10)),
        sa.Column('Age', sa.Integer),
        sa.Column('Job', sa.Integer), # 직업의 유형별로 분류하여 숫자로 인코딩 할 예정
        sa.Column('Sex', sa.Integer)
    )


def downgrade():
    pass
