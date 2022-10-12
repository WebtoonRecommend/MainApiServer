"""change_thumb

Revision ID: 9e86ed1eb745
Revises: 1eba6cdcb1d8
Create Date: 2022-10-12 09:52:49.717074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e86ed1eb745'
down_revision = '1eba6cdcb1d8'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('web_toon', 'ThumbNail')
    op.add_column('web_toon', sa.Column('ThumbNail', sa.String(100)))


def downgrade():
    pass
