"""create_base_tables

Revision ID: 000000000000
Revises:
Create Date: 2026-05-31 19:54:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '000000000000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('competencias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('tipo', sa.String(length=50), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('peso', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_competencias_nome'), 'competencias', ['nome'], unique=False)
    
    op.create_table('execucoes_agente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agente_nome', sa.String(length=100), nullable=False),
    sa.Column('entidade_tipo', sa.String(length=100), nullable=False),
    sa.Column('entidade_id', sa.Integer(), nullable=False),
    sa.Column('entrada', sa.JSON(), nullable=True),
    sa.Column('saida', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('erro', sa.Text(), nullable=True),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('funcoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_funcoes_nome'), 'funcoes', ['nome'], unique=True)
    
    op.create_table('setores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_setores_nome'), 'setores', ['nome'], unique=True)
    
    op.create_table('colaboradores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('matricula', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('data_admissao', sa.Date(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('setor_id', sa.Integer(), nullable=False),
    sa.Column('funcao_id', sa.Integer(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['funcao_id'], ['funcoes.id'], ),
    sa.ForeignKeyConstraint(['setor_id'], ['setores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_colaboradores_email'), 'colaboradores', ['email'], unique=True)
    op.create_index(op.f('ix_colaboradores_matricula'), 'colaboradores', ['matricula'], unique=True)
    
    op.create_table('perfis_talento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('colaborador_id', sa.Integer(), nullable=False),
    sa.Column('classificacao', sa.String(length=80), nullable=False),
    sa.Column('resumo', sa.Text(), nullable=True),
    sa.Column('nivel_tecnico', sa.String(length=30), nullable=True),
    sa.Column('nivel_comportamental', sa.String(length=30), nullable=True),
    sa.Column('potencial_lideranca', sa.String(length=30), nullable=True),
    sa.Column('pontos_fortes', sa.JSON(), nullable=True),
    sa.Column('pontos_melhoria', sa.JSON(), nullable=True),
    sa.Column('recomendacoes', sa.JSON(), nullable=True),
    sa.Column('origem', sa.String(length=50), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['colaborador_id'], ['colaboradores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('senha_hash', sa.String(length=255), nullable=False),
    sa.Column('perfil', sa.String(length=50), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    
    op.create_table('avaliacoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('colaborador_id', sa.Integer(), nullable=False),
    sa.Column('avaliador_id', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.String(length=50), nullable=False),
    sa.Column('observacao_geral', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('data_avaliacao', sa.DateTime(timezone=True), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['avaliador_id'], ['usuarios.id'], ),
    sa.ForeignKeyConstraint(['colaborador_id'], ['colaboradores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('feedbacks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('colaborador_id', sa.Integer(), nullable=False),
    sa.Column('autor_id', sa.Integer(), nullable=False),
    sa.Column('contexto', sa.Text(), nullable=True),
    sa.Column('ponto_positivo', sa.Text(), nullable=False),
    sa.Column('ponto_melhoria', sa.Text(), nullable=True),
    sa.Column('acao_recomendada', sa.Text(), nullable=False),
    sa.Column('origem', sa.String(length=50), nullable=False),
    sa.Column('data_feedback', sa.DateTime(timezone=True), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['autor_id'], ['usuarios.id'], ),
    sa.ForeignKeyConstraint(['colaborador_id'], ['colaboradores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('metas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('colaborador_id', sa.Integer(), nullable=False),
    sa.Column('criado_por_id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=150), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.Column('indicador', sa.String(length=150), nullable=True),
    sa.Column('prazo', sa.Date(), nullable=False),
    sa.Column('prioridade', sa.String(length=30), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('origem', sa.String(length=50), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['colaborador_id'], ['colaboradores.id'], ),
    sa.ForeignKeyConstraint(['criado_por_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('itens_avaliacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('avaliacao_id', sa.Integer(), nullable=False),
    sa.Column('competencia_id', sa.Integer(), nullable=False),
    sa.Column('nota', sa.Integer(), nullable=False),
    sa.Column('comentario', sa.Text(), nullable=True),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['avaliacao_id'], ['avaliacoes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['competencia_id'], ['competencias.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('itens_avaliacao')
    op.drop_table('metas')
    op.drop_table('feedbacks')
    op.drop_table('avaliacoes')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')
    op.drop_table('perfis_talento')
    op.drop_index(op.f('ix_colaboradores_matricula'), table_name='colaboradores')
    op.drop_index(op.f('ix_colaboradores_email'), table_name='colaboradores')
    op.drop_table('colaboradores')
    op.drop_index(op.f('ix_setores_nome'), table_name='setores')
    op.drop_table('setores')
    op.drop_index(op.f('ix_funcoes_nome'), table_name='funcoes')
    op.drop_table('funcoes')
    op.drop_table('execucoes_agente')
    op.drop_index(op.f('ix_competencias_nome'), table_name='competencias')
    op.drop_table('competencias')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
