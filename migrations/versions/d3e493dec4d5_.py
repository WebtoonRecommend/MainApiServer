"""empty message

Revision ID: d3e493dec4d5
Revises: 
Create Date: 2022-09-24 16:45:27.217894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3e493dec4d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('ID', sa.String(length=10), nullable=False),
    sa.Column('PassWd', sa.String(length=10), nullable=True),
    sa.Column('Age', sa.Integer(), nullable=True),
    sa.Column('Job', sa.Integer(), nullable=True),
    sa.Column('Sex', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('web_toon',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Author', sa.String(length=10), nullable=True),
    sa.Column('Title', sa.String(length=10), nullable=False),
    sa.Column('Summary', sa.String(length=100), nullable=True),
    sa.Column('ThumbNail', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('world_cup',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Round', sa.Integer(), nullable=True),
    sa.Column('UID', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('world_cup')
    op.drop_table('web_toon')
    op.drop_table('user')
    # ### end Alembic commands ###
