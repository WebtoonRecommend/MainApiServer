"""resetAgain

Revision ID: d42b34f31023
Revises: f1785a5deea6
Create Date: 2022-09-30 14:11:22.103347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd42b34f31023'
down_revision = 'f1785a5deea6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'web_toon',
        sa.Column('ID', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('Author', sa.String(10)),
        sa.Column('Title', sa.String(10)),
        sa.Column('Summary', sa.String(100)), # 직업의 유형별로 분류하여 숫자로 인코딩 할 예정
        sa.Column('ThumbNail', sa.String(20))
    )

    op.create_table(
        'world_cup',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('Round', sa.Integer),
        sa.Column('UID', sa.String(10)),
        sa.Column('WebtoonTitle', sa.String(10))
    )

    op.create_table(
        'book_mark',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('UID', sa.String(10)),
        sa.Column('WebtoonTitle', sa.String(10))
    )
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
