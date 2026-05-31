from domain.entities.pdi import PDI
from domain.entities.acao_pdi import AcaoPDI
from domain.enums.pdi_enums import StatusPDI, OrigemPDI, TipoAcaoPDI, StatusAcaoPDI
from application.dtos.pdi_dto import (
    CriarPDIDTO,
    AtualizarPDIDTO,
    CriarAcaoPDIDTO,
    AtualizarAcaoPDIDTO,
)
from application.errors import NotFoundError, ValidationError


class CriarPDIUC:
    def __init__(self, colaboradores_repo, usuarios_repo, pdis_repo):
        self.colaboradores_repo = colaboradores_repo
        self.usuarios_repo = usuarios_repo
        self.pdis_repo = pdis_repo

    def execute(self, dto: CriarPDIDTO) -> PDI:
        if not dto.titulo:
            raise ValidationError("Titulo do PDI e obrigatorio.")
        if not dto.descricao:
            raise ValidationError("Descricao do PDI e obrigatorio.")

        colaborador = self.colaboradores_repo.get_by_id(dto.colaborador_id)
        if not colaborador:
            raise NotFoundError("Colaborador nao encontrado.")

        usuario = self.usuarios_repo.get_by_id(dto.criado_por_id)
        if not usuario:
            raise NotFoundError("Usuario criador nao encontrado.")

        try:
            origem = OrigemPDI(dto.origem)
        except ValueError:
            raise ValidationError(f"Origem '{dto.origem}' e invalida.")

        try:
            status = StatusPDI(dto.status)
        except ValueError:
            raise ValidationError(f"Status '{dto.status}' e invalido.")

        if status not in (StatusPDI.RASCUNHO, StatusPDI.ATIVO):
            raise ValidationError("PDI novo deve iniciar como RASCUNHO ou ATIVO.")

        acoes_domain = []
        if dto.acoes:
            for acao_dto in dto.acoes:
                if not acao_dto.descricao:
                    raise ValidationError("Descricao da acao e obrigatoria.")
                if not acao_dto.tipo:
                    raise ValidationError("Tipo da acao e obrigatorio.")
                if not acao_dto.prazo:
                    raise ValidationError("Prazo da acao e obrigatorio.")
                try:
                    tipo_acao = TipoAcaoPDI(acao_dto.tipo)
                except ValueError:
                    raise ValidationError(f"Tipo de acao '{acao_dto.tipo}' e invalido.")
                acoes_domain.append(
                    AcaoPDI(
                        tipo=tipo_acao,
                        descricao=acao_dto.descricao,
                        prazo=acao_dto.prazo,
                        status=StatusAcaoPDI.PENDENTE,
                    )
                )

        pdi = PDI(
            colaborador_id=dto.colaborador_id,
            titulo=dto.titulo,
            descricao=dto.descricao,
            criado_por_id=dto.criado_por_id,
            origem=origem,
            status=status,
            data_inicio=dto.data_inicio,
            data_fim=dto.data_fim,
            acoes=acoes_domain,
        )
        return self.pdis_repo.add(pdi)


class ListarPDIsUC:
    def __init__(self, pdis_repo):
        self.pdis_repo = pdis_repo

    def execute(self) -> list[PDI]:
        return self.pdis_repo.list_all()


class BuscarPDIUC:
    def __init__(self, pdis_repo):
        self.pdis_repo = pdis_repo

    def execute(self, pdi_id: int) -> PDI:
        pdi = self.pdis_repo.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")
        return pdi


class ListarPDIsPorColaboradorUC:
    def __init__(self, pdis_repo):
        self.pdis_repo = pdis_repo

    def execute(self, colaborador_id: int) -> list[PDI]:
        return self.pdis_repo.list_by_colaborador_id(colaborador_id)


class AtualizarPDIUC:
    def __init__(self, pdis_repo):
        self.pdis_repo = pdis_repo

    def execute(self, dto: AtualizarPDIDTO) -> PDI:
        pdi = self.pdis_repo.get_by_id(dto.id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        if pdi.status == StatusPDI.CONCLUIDO:
            raise ValidationError("PDI concluido nao pode ser alterado.")
        if pdi.status == StatusPDI.CANCELADO:
            raise ValidationError("PDI cancelado nao pode ser alterado.")

        if not dto.titulo:
            raise ValidationError("Titulo do PDI e obrigatorio.")
        if not dto.descricao:
            raise ValidationError("Descricao do PDI e obrigatorio.")

        pdi.titulo = dto.titulo
        pdi.descricao = dto.descricao
        pdi.data_inicio = dto.data_inicio
        pdi.data_fim = dto.data_fim

        self.pdis_repo.save(pdi)
        return pdi


class ConcluirPDIUC:
    def __init__(self, pdis_repo):
        self.pdis_repo = pdis_repo

    def execute(self, pdi_id: int) -> PDI:
        pdi = self.pdis_repo.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        try:
            pdi.concluir()
        except ValueError as exc:
            raise ValidationError(str(exc))

        self.pdis_repo.save(pdi)
        return pdi


class CancelarPDIUC:
    def __init__(self, pdis_repo):
        self.pdis_repo = pdis_repo

    def execute(self, pdi_id: int) -> PDI:
        pdi = self.pdis_repo.get_by_id(pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        try:
            pdi.cancelar()
        except ValueError as exc:
            raise ValidationError(str(exc))

        self.pdis_repo.save(pdi)
        return pdi


class CriarAcaoPDIUC:
    def __init__(self, pdis_repo, acoes_pdi_repo):
        self.pdis_repo = pdis_repo
        self.acoes_pdi_repo = acoes_pdi_repo

    def execute(self, dto: CriarAcaoPDIDTO) -> AcaoPDI:
        pdi = self.pdis_repo.get_by_id(dto.pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        if pdi.status == StatusPDI.CONCLUIDO:
            raise ValidationError("PDI concluido nao permite alteracao.")
        if pdi.status == StatusPDI.CANCELADO:
            raise ValidationError("PDI cancelado nao permite alteracao.")

        if not dto.descricao:
            raise ValidationError("Descricao da acao e obrigatoria.")
        if not dto.tipo:
            raise ValidationError("Tipo da acao e obrigatorio.")
        if not dto.prazo:
            raise ValidationError("Prazo da acao e obrigatorio.")

        try:
            tipo_acao = TipoAcaoPDI(dto.tipo)
        except ValueError:
            raise ValidationError(f"Tipo de acao '{dto.tipo}' e invalido.")

        acao = AcaoPDI(
            pdi_id=dto.pdi_id,
            tipo=tipo_acao,
            descricao=dto.descricao,
            prazo=dto.prazo,
            status=StatusAcaoPDI.PENDENTE,
        )
        return self.acoes_pdi_repo.add(acao)


class AtualizarAcaoPDIUC:
    def __init__(self, pdis_repo, acoes_pdi_repo):
        self.pdis_repo = pdis_repo
        self.acoes_pdi_repo = acoes_pdi_repo

    def execute(self, dto: AtualizarAcaoPDIDTO) -> AcaoPDI:
        acao = self.acoes_pdi_repo.get_by_id(dto.id)
        if not acao:
            raise NotFoundError("Acao nao encontrada.")

        pdi = self.pdis_repo.get_by_id(acao.pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        if pdi.status == StatusPDI.CONCLUIDO:
            raise ValidationError("PDI concluido nao permite alteracao.")
        if pdi.status == StatusPDI.CANCELADO:
            raise ValidationError("PDI cancelado nao permite alteracao.")

        if not dto.descricao:
            raise ValidationError("Descricao da acao e obrigatoria.")
        if not dto.tipo:
            raise ValidationError("Tipo da acao e obrigatorio.")
        if not dto.prazo:
            raise ValidationError("Prazo da acao e obrigatorio.")

        try:
            tipo_acao = TipoAcaoPDI(dto.tipo)
        except ValueError:
            raise ValidationError(f"Tipo de acao '{dto.tipo}' e invalido.")

        acao.tipo = tipo_acao
        acao.descricao = dto.descricao
        acao.prazo = dto.prazo

        self.acoes_pdi_repo.save(acao)
        return acao


class ConcluirAcaoPDIUC:
    def __init__(self, pdis_repo, acoes_pdi_repo):
        self.pdis_repo = pdis_repo
        self.acoes_pdi_repo = acoes_pdi_repo

    def execute(self, acao_id: int) -> AcaoPDI:
        acao = self.acoes_pdi_repo.get_by_id(acao_id)
        if not acao:
            raise NotFoundError("Acao nao encontrada.")

        pdi = self.pdis_repo.get_by_id(acao.pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        if pdi.status == StatusPDI.CONCLUIDO:
            raise ValidationError("PDI concluido nao permite alteracao.")
        if pdi.status == StatusPDI.CANCELADO:
            raise ValidationError("PDI cancelado nao permite alteracao.")

        try:
            acao.concluir()
        except ValueError as exc:
            raise ValidationError(str(exc))

        self.acoes_pdi_repo.save(acao)
        return acao


class CancelarAcaoPDIUC:
    def __init__(self, pdis_repo, acoes_pdi_repo):
        self.pdis_repo = pdis_repo
        self.acoes_pdi_repo = acoes_pdi_repo

    def execute(self, acao_id: int) -> AcaoPDI:
        acao = self.acoes_pdi_repo.get_by_id(acao_id)
        if not acao:
            raise NotFoundError("Acao nao encontrada.")

        pdi = self.pdis_repo.get_by_id(acao.pdi_id)
        if not pdi:
            raise NotFoundError("PDI nao encontrado.")

        if pdi.status == StatusPDI.CONCLUIDO:
            raise ValidationError("PDI concluido nao permite alteracao.")
        if pdi.status == StatusPDI.CANCELADO:
            raise ValidationError("PDI cancelado nao permite alteracao.")

        try:
            acao.cancelar()
        except ValueError as exc:
            raise ValidationError(str(exc))

        self.acoes_pdi_repo.save(acao)
        return acao
