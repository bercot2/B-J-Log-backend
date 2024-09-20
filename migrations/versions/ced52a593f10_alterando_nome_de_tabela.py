"""alterando nome de tabela

Revision ID: ced52a593f10
Revises: e278a8f715b5
Create Date: 2024-09-20 14:13:53.939334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ced52a593f10'
down_revision = 'e278a8f715b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authentication',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('chave_acesso', sa.String(length=50), nullable=False),
    sa.Column('secret_key', sa.String(), nullable=False),
    sa.Column('pode_gerar_token', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chave_acesso'),
    sa.UniqueConstraint('nome')
    )
    op.drop_table('token_authentication')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_authentication',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('chave_acesso', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('secret_key', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('pode_gerar_token', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='token_authentication_pkey'),
    sa.UniqueConstraint('chave_acesso', name='token_authentication_chave_acesso_key'),
    sa.UniqueConstraint('nome', name='token_authentication_nome_key')
    )
    op.drop_table('authentication')
    # ### end Alembic commands ###
