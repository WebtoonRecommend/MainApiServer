"""AddAllDBS

Revision ID: 90c19cff8625
Revises: bd4e2f88fed4
Create Date: 2022-09-29 00:07:28.421334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90c19cff8625'
down_revision = 'bd4e2f88fed4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'WebToon',
        sa.Column('ID', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('Author', sa.String(10)),
        sa.Column('Title', sa.String(10)),
        sa.Column('Summary', sa.String(100)), # 직업의 유형별로 분류하여 숫자로 인코딩 할 예정
        sa.Column('ThumbNail', sa.String(20))
    )

    op.create_table(
        'WorldCup',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('Round', sa.Integer),
        sa.Column('UID', sa.String(10)),
        sa.Column('WebtoonTitle', sa.String(10))
    )

    op.create_table(
        'BookMark',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('UID', sa.String(10)),
        sa.Column('WebtoonTitle', sa.String(10))
    )


def downgrade():
    pass
