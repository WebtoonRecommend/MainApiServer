"""deleteImage

Revision ID: f165fbedf0d2
Revises: 13d8de11bef0
Create Date: 2022-10-09 19:07:54.974409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f165fbedf0d2'
down_revision = '13d8de11bef0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('web_toon', 'UID')
    op.add_column('web_toon', sa.Column('ThumbNail', sa.String(100)))


def downgrade():
    pass
