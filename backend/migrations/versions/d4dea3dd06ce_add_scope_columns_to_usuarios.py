"""add_scope_columns_to_usuarios

Revision ID: d4dea3dd06ce
Revises: 
Create Date: 2026-05-31 17:26:02.835274
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4dea3dd06ce'
down_revision: Union[str, None] = '000000000000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('usuarios', sa.Column('colaborador_id', sa.Integer(), nullable=True))
    op.add_column('usuarios', sa.Column('setor_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_usuarios_colaborador_id', 'usuarios', 'colaboradores', ['colaborador_id'], ['id'])
    op.create_foreign_key('fk_usuarios_setor_id', 'usuarios', 'setores', ['setor_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_usuarios_setor_id', 'usuarios', type_='foreignkey')
    op.drop_constraint('fk_usuarios_colaborador_id', 'usuarios', type_='foreignkey')
    op.drop_column('usuarios', 'setor_id')
    op.drop_column('usuarios', 'colaborador_id')
