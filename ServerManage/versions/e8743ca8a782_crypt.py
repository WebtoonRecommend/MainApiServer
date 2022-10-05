"""crypt

Revision ID: e8743ca8a782
Revises: 17e34d7187f9
Create Date: 2022-10-05 10:34:26.735207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8743ca8a782'
down_revision = '17e34d7187f9'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('world_cup', 'UID')
    op.add_column('world_cup', sa.Column('UID', sa.String(100)))
    op.drop_column('book_mark', 'UID')
    op.add_column('book_mark', sa.Column('UID', sa.String(100)))
    op.drop_column('recommended_list', 'UID')
    op.add_column('recommended_', sa.Column('UID', sa.String(100)))
    op.drop_table('user')
    op.create_table(
        'user',
        sa.Column('ID', sa.String(100), primary_key=True),
        sa.Column('PassWd', sa.String(100)),
        sa.Column('Age', sa.Integer),
        sa.Column('Job', sa.Integer), # 직업의 유형별로 분류하여 숫자로 인코딩 할 예정
        sa.Column('Sex', sa.Integer)
    )


def downgrade():
    pass
