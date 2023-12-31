"""empty message

Revision ID: 5ca0acd9e32d
Revises: 70623e151780
Create Date: 2023-08-23 14:11:27.041616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ca0acd9e32d'
down_revision = '70623e151780'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=345), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
