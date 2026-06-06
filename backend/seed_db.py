import os
import sys
from datetime import date, datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from domain.enums.perfil_usuario import PerfilUsuario
from domain.enums.status_meta import StatusMeta
from domain.enums.prioridade_meta import PrioridadeMeta
from domain.enums.pdi_enums import StatusPDI, OrigemPDI
from domain.enums.tipo_reconhecimento import TipoReconhecimento

from infrastructure.database.models.usuario_model import UsuarioModel
from infrastructure.database.models.colaborador_model import ColaboradorModel
from infrastructure.database.models.setor_model import SetorModel
from infrastructure.database.models.funcao_model import FuncaoModel
from infrastructure.database.models.meta_model import MetaModel
from infrastructure.database.models.feedback_model import FeedbackModel
from infrastructure.database.models.pdi_model import PDIModel
from infrastructure.database.models.reconhecimento_model import ReconhecimentoModel

from werkzeug.security import generate_password_hash

def seed():
    app = create_app()
    with app.app_context():
        print("Cleaning old seed data...")
        # Delete existing data in proper dependency order
        db.session.query(ReconhecimentoModel).delete()
        db.session.query(PDIModel).delete()
        db.session.query(FeedbackModel).delete()
        db.session.query(MetaModel).delete()
        db.session.query(UsuarioModel).delete()
        db.session.query(ColaboradorModel).delete()
        db.session.query(FuncaoModel).delete()
        db.session.query(SetorModel).delete()
        db.session.commit()

        print("Seeding new database data...")
        admin_pw = generate_password_hash("admin123")
        rh_pw = generate_password_hash("rh123")
        lider_pw = generate_password_hash("lider123")
        colab_pw = generate_password_hash("colab123")
        inactive_pw = generate_password_hash("inactive123")

        # 1. Seed Sectors
        setor1 = SetorModel(nome="Engenharia", descricao="Setor de Engenharia de Software")
        setor2 = SetorModel(nome="Marketing", descricao="Setor de Marketing Digital")
        db.session.add_all([setor1, setor2])
        db.session.commit()

        # 2. Seed Functions
        funcao1 = FuncaoModel(nome="Desenvolvedor", descricao="Desenvolvedor Full Stack")
        funcao2 = FuncaoModel(nome="Analista de Marketing", descricao="Analista de Mídias Sociais")
        db.session.add_all([funcao1, funcao2])
        db.session.commit()

        # 3. Seed Collaborators
        colab1 = ColaboradorModel(
            nome="Colaborador A (Engenharia)",
            matricula="M001",
            email="colaba@test.com",
            data_admissao=date(2026, 1, 1),
            status="ATIVO",
            setor_id=setor1.id,
            funcao_id=funcao1.id,
        )
        colab2 = ColaboradorModel(
            nome="Colaborador B (Marketing)",
            matricula="M002",
            email="colabb@test.com",
            data_admissao=date(2026, 1, 1),
            status="ATIVO",
            setor_id=setor2.id,
            funcao_id=funcao2.id,
        )
        db.session.add_all([colab1, colab2])
        db.session.commit()

        # 4. Seed Users
        admin_user = UsuarioModel(
            nome="Admin User",
            email="admin@test.com",
            senha_hash=admin_pw,
            perfil=PerfilUsuario.ADMIN.value,
            ativo=True,
        )
        rh_user = UsuarioModel(
            nome="RH User",
            email="rh@test.com",
            senha_hash=rh_pw,
            perfil=PerfilUsuario.RH.value,
            ativo=True,
        )
        lider_a = UsuarioModel(
            nome="Lider A (Engenharia)",
            email="lidera@test.com",
            senha_hash=lider_pw,
            perfil=PerfilUsuario.LIDER.value,
            ativo=True,
            setor_id=setor1.id,
        )
        colab_user = UsuarioModel(
            nome="Colab User",
            email="colab@test.com",
            senha_hash=colab_pw,
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=True,
            colaborador_id=colab1.id,
        )
        inactive_user = UsuarioModel(
            nome="Inactive User",
            email="inactive@test.com",
            senha_hash=inactive_pw,
            perfil=PerfilUsuario.COLABORADOR.value,
            ativo=False,
        )
        db.session.add_all([admin_user, rh_user, lider_a, colab_user, inactive_user])
        db.session.commit()

        # 5. Seed Metas, PDIs, Feedbacks, and Reconhecimentos for Colab A (under Lider A's sector)
        m1 = MetaModel(
            colaborador_id=colab1.id,
            criado_por_id=admin_user.id,
            titulo="Meta de Engenharia 1",
            descricao="Entrega da Sprint 1",
            prazo=date(2026, 6, 15),
            status=StatusMeta.EM_ANDAMENTO.value,
            prioridade=PrioridadeMeta.ALTA.value,
            origem="MANUAL"
        )
        db.session.add(m1)

        f1 = FeedbackModel(
            colaborador_id=colab1.id,
            autor_id=lider_a.id,
            contexto="Excelente dedicação no código",
            ponto_positivo="Qualidade",
            ponto_melhoria="Documentação",
            acao_recomendada="Escrever testes",
            data_feedback=datetime(2026, 5, 20, 14, 30),
            criado_em=datetime(2026, 5, 20, 14, 30)
        )
        db.session.add(f1)

        pdi1 = PDIModel(
            colaborador_id=colab1.id,
            criado_por_id=lider_a.id,
            titulo="PDI de Engenharia 1",
            descricao="Desenvolvimento de Soft Skills",
            origem=OrigemPDI.AVALIACAO.value,
            status=StatusPDI.ATIVO.value,
            data_inicio=date(2026, 5, 1),
            data_fim=date(2026, 8, 1),
            criado_em=datetime(2026, 5, 1, 9, 0)
        )
        db.session.add(pdi1)

        r1 = ReconhecimentoModel(
            colaborador_id=colab1.id,
            registrado_por_id=lider_a.id,
            tipo=TipoReconhecimento.DESTAQUE.value,
            descricao="Destaque técnico na arquitetura do backend",
            evidencia="Pull requests aprovados",
            data_reconhecimento=datetime(2026, 5, 25, 16, 0),
            criado_em=datetime(2026, 5, 25, 16, 0),
            ativo=True
        )
        db.session.add(r1)

        # 6. Seed Meta for Colab B (Marketing - outside Lider A's sector)
        m2 = MetaModel(
            colaborador_id=colab2.id,
            criado_por_id=admin_user.id,
            titulo="Meta de Marketing 1",
            descricao="Campanha de Redes Sociais",
            prazo=date(2026, 6, 20),
            status=StatusMeta.PENDENTE.value,
            prioridade=PrioridadeMeta.MEDIA.value,
            origem="MANUAL"
        )
        db.session.add(m2)

        db.session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed()
