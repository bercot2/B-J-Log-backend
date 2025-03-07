"""Adicionando colunas de permissoes de usuario

Revision ID: 6c3cc79bb01c
Revises: a0bbed1af41d
Create Date: 2024-09-20 00:47:26.708675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c3cc79bb01c'
down_revision = 'a0bbed1af41d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_staff', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('is_superuser', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('is_superuser')
        batch_op.drop_column('is_staff')

    # ### end Alembic commands ###
