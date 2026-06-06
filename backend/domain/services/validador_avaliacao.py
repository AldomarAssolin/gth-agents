from domain.enums.tipo_avaliacao import TipoAvaliacao


class ValidadorAvaliacao:
    def validar(self, avaliacao) -> None:
        if avaliacao.colaborador_id is None:
            raise ValueError("avaliacao must be linked to a colaborador")
        if avaliacao.avaliador_id is None:
            raise ValueError("avaliacao must have an avaliador")
        if not avaliacao.itens:
            raise ValueError("avaliacao must contain at least one item")

        competencias_avaliadas = set()
        for item in avaliacao.itens:
            if item.competencia_id in competencias_avaliadas:
                raise ValueError("competencia cannot be evaluated twice")
            competencias_avaliadas.add(item.competencia_id)

            if item.nota < 1 or item.nota > 5:
                raise ValueError("nota must be between 1 and 5")

    def validar_tipo(self, tipo: str) -> str:
        tipo_normalizado = (tipo or TipoAvaliacao.AVALIACAO_LIDER.value).upper()

        if tipo_normalizado not in TipoAvaliacao._value2member_map_:
            valores = ", ".join(item.value for item in TipoAvaliacao)
            raise ValueError(f"tipo must be one of: {valores}")

        return tipo_normalizado

    def validar_itens(self, itens: list[dict]) -> None:
        if not itens:
            raise ValueError("itens must contain at least one item")

        for item in itens:
            nota = item.get("nota")
            if not isinstance(nota, int) or nota < 1 or nota > 5:
                raise ValueError("nota must be an integer between 1 and 5")
