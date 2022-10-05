"""keyword

Revision ID: 13d8de11bef0
Revises: e8743ca8a782
Create Date: 2022-10-05 22:23:07.488154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13d8de11bef0'
down_revision = 'e8743ca8a782'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'key_words',
        sa.Column('ID', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('UID', sa.String(10)),
        sa.Column('Word', sa.String(10))
    )


def downgrade():
    pass
