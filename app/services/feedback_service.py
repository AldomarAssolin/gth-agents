from app.repositories.domain_repositories import ColaboradorRepository, FeedbackRepository, UsuarioRepository
from app.services.agents import AgenteFeedback


class FeedbackService:
    def __init__(self):
        self.repository = FeedbackRepository()
        self.colaboradores = ColaboradorRepository()
        self.usuarios = UsuarioRepository()
        self.agente_feedback = AgenteFeedback()

    def list(self):
        return self.repository.list()

    def create(self, data: dict):
        if not self.colaboradores.get(data.get("colaborador_id")):
            raise ValueError("colaborador_id not found")
        if not self.usuarios.get(data.get("autor_id")):
            raise ValueError("autor_id not found")
        if not data.get("ponto_positivo"):
            raise ValueError("ponto_positivo is required")
        if not data.get("acao_recomendada"):
            raise ValueError("acao_recomendada is required")

        payload = data.copy()
        payload["origem"] = payload.get("origem") or "MANUAL"
        return self.repository.create(**payload)

    def estruturar_observacao(self, observacao: str):
        return self.agente_feedback.estruturar(observacao)
