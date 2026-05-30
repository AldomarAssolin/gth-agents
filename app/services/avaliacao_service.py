from app.extensions import db
from app.models import Avaliacao, ExecucaoAgente, ItemAvaliacao, Meta, PerfilTalento
from app.repositories.domain_repositories import (
    AvaliacaoRepository,
    ColaboradorRepository,
    CompetenciaRepository,
    UsuarioRepository,
)
from app.services.agents import AgenteAvaliador, AgenteGeradorMetas, AgentePerfilador
from domain.services.validador_avaliacao import ValidadorAvaliacao


class AvaliacaoService:
    def __init__(self):
        self.repository = AvaliacaoRepository()
        self.colaboradores = ColaboradorRepository()
        self.usuarios = UsuarioRepository()
        self.competencias = CompetenciaRepository()
        self.agente_avaliador = AgenteAvaliador()
        self.agente_perfilador = AgentePerfilador()
        self.agente_metas = AgenteGeradorMetas()
        self.validador = ValidadorAvaliacao()

    def list(self):
        return self.repository.list()

    def get(self, avaliacao_id: int):
        avaliacao = self.repository.get(avaliacao_id)
        if not avaliacao:
            raise ValueError("avaliacao not found")
        return avaliacao

    def create(self, data: dict):
        colaborador = self.colaboradores.get(data.get("colaborador_id"))
        avaliador = self.usuarios.get(data.get("avaliador_id"))
        itens = data.get("itens") or []
        tipo = self.validador.validar_tipo(data.get("tipo"))
        self.validador.validar_itens(itens)

        if not colaborador:
            raise ValueError("colaborador_id not found")
        if not avaliador:
            raise ValueError("avaliador_id not found")

        avaliacao = Avaliacao(
            colaborador_id=colaborador.id,
            avaliador_id=avaliador.id,
            tipo=tipo,
            observacao_geral=data.get("observacao_geral"),
            status=data.get("status") or "CONCLUIDA",
        )

        for item_data in itens:
            competencia = self.competencias.get(item_data.get("competencia_id"))
            nota = item_data.get("nota")

            if not competencia:
                raise ValueError("competencia_id not found")
            avaliacao.itens.append(
                ItemAvaliacao(
                    competencia_id=competencia.id,
                    nota=nota,
                    comentario=item_data.get("comentario"),
                )
            )

        db.session.add(avaliacao)
        db.session.flush()

        analise = self.agente_avaliador.analisar(colaborador, avaliacao)
        perfil_data = self.agente_perfilador.classificar(analise)
        perfil = PerfilTalento(colaborador_id=colaborador.id, **perfil_data)
        db.session.add(perfil)
        db.session.flush()

        metas = []
        for meta_data in self.agente_metas.sugerir(perfil_data):
            meta = Meta(colaborador_id=colaborador.id, criado_por_id=avaliador.id, **meta_data)
            db.session.add(meta)
            metas.append(meta)

        self._registrar_execucao("Agente Avaliador", "avaliacao", avaliacao.id, data, analise)
        self._registrar_execucao("Agente Perfilador", "perfil_talento", perfil.id, analise, perfil_data)
        self._registrar_execucao("Agente Gerador de Metas", "colaborador", colaborador.id, perfil_data, {"metas": [m.titulo for m in metas]})

        db.session.commit()
        return {"avaliacao": avaliacao, "perfil": perfil, "metas": metas}

    def _registrar_execucao(self, agente_nome: str, entidade_tipo: str, entidade_id: int, entrada, saida):
        db.session.add(
            ExecucaoAgente(
                agente_nome=agente_nome,
                entidade_tipo=entidade_tipo,
                entidade_id=entidade_id,
                entrada=entrada,
                saida=saida,
            )
        )
