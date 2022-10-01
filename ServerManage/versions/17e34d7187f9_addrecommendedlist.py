"""addRecommendedList

Revision ID: 17e34d7187f9
Revises: 1c22ceb1814b
Create Date: 2022-10-02 00:37:56.933185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17e34d7187f9'
down_revision = '1c22ceb1814b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'recommended_list',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('UID', sa.String(10)),
        sa.Column('WebtoonTitle', sa.String(10))
    )


def downgrade():
    pass
