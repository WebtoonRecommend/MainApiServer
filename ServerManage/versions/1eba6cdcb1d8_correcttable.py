"""correcttable

Revision ID: 1eba6cdcb1d8
Revises: f165fbedf0d2
Create Date: 2022-10-09 19:18:26.760753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eba6cdcb1d8'
down_revision = 'f165fbedf0d2'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('web_toon', 'UID')
    op.add_column('web_toon', sa.Column('ThumbNail', sa.String(100)))


def downgrade():
    pass
