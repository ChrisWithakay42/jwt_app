"""empty message

Revision ID: 4de7db5827a8
Revises: 8de9c62b2a3c
Create Date: 2023-08-22 11:08:30.045674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4de7db5827a8'
down_revision = '8de9c62b2a3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('magic_link',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('user_uuid', sa.UUID(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.String(length=120), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_uuid')
    )
    op.create_table('to_do',
    sa.Column('text', sa.String(length=150), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('to_do')
    op.drop_table('user')
    op.drop_table('magic_link')
    # ### end Alembic commands ###
