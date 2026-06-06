from decimal import Decimal
import pytest
from domain.entities.avaliacao import Avaliacao
from domain.entities.item_avaliacao import ItemAvaliacao
from domain.entities.competencia import Competencia
from domain.enums.tipo_competencia import TipoCompetencia
from domain.enums.tipo_avaliacao import TipoAvaliacao
from domain.services.calculadora_competencias import CalculadoraCompetencias


def make_competencia(id: int, tipo: TipoCompetencia, peso: float = 1.0) -> Competencia:
    return Competencia(
        id=id,
        nome=f"Competencia {id}",
        tipo=tipo,
        peso=Decimal(str(peso)),
        ativo=True,
    )


# 1. Calculates simple technical average correctly.
def test_calcula_media_tecnica_simples():
    calc = CalculadoraCompetencias()
    c1 = make_competencia(1, TipoCompetencia.TECNICA, peso=1.0)
    c2 = make_competencia(2, TipoCompetencia.TECNICA, peso=1.0)

    avaliacao = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=5.0),
            ItemAvaliacao(competencia_id=2, nota=3.0),
        ],
    )

    resultado = calc.calcular(avaliacao, {1: c1, 2: c2})
    assert resultado.media_tecnica == 4.0
    assert resultado.media_geral == 4.0


# 2. Calculates simple behavioral average correctly.
def test_calcula_media_comportamental_simples():
    calc = CalculadoraCompetencias()
    c1 = make_competencia(1, TipoCompetencia.COMPORTAMENTAL, peso=1.0)
    c2 = make_competencia(2, TipoCompetencia.COMPORTAMENTAL, peso=1.0)

    avaliacao = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=4.0),
            ItemAvaliacao(competencia_id=2, nota=2.0),
        ],
    )

    resultado = calc.calcular(avaliacao, {1: c1, 2: c2})
    assert resultado.media_comportamental == 3.0
    assert resultado.media_geral == 3.0


# 3. Calculates simple leadership average correctly.
def test_calcula_media_lideranca_simples():
    calc = CalculadoraCompetencias()
    c1 = make_competencia(1, TipoCompetencia.LIDERANCA, peso=1.0)
    c2 = make_competencia(2, TipoCompetencia.LIDERANCA, peso=1.0)

    avaliacao = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=4.0),
            ItemAvaliacao(competencia_id=2, nota=5.0),
        ],
    )

    resultado = calc.calcular(avaliacao, {1: c1, 2: c2})
    assert resultado.media_lideranca == 4.5
    assert resultado.media_geral == 4.5


# 4. Calculates simple organizational average correctly.
def test_calcula_media_organizacional_simples():
    calc = CalculadoraCompetencias()
    c1 = make_competencia(1, TipoCompetencia.ORGANIZACIONAL, peso=1.0)
    c2 = make_competencia(2, TipoCompetencia.ORGANIZACIONAL, peso=1.0)

    avaliacao = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=3.0),
            ItemAvaliacao(competencia_id=2, nota=4.0),
        ],
    )

    resultado = calc.calcular(avaliacao, {1: c1, 2: c2})
    assert resultado.media_organizacional == 3.5
    assert resultado.media_geral == 3.5


# 5. Calculates weighted average correctly.
def test_calcula_media_ponderada_corretamente():
    calc = CalculadoraCompetencias()
    c1 = make_competencia(1, TipoCompetencia.TECNICA, peso=2.0)
    c2 = make_competencia(2, TipoCompetencia.TECNICA, peso=1.0)

    avaliacao = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=5.0),
            ItemAvaliacao(competencia_id=2, nota=2.0),
        ],
    )

    resultado = calc.calcular(avaliacao, {1: c1, 2: c2})
    # media = ((5 * 2) + (2 * 1)) / (2 + 1) = 12 / 3 = 4.0
    assert resultado.media_tecnica == 4.0
    assert resultado.media_geral == 4.0


# 6. Competency with weight 2 influences more than competency with weight 1.
def test_peso_influencia_mais():
    calc = CalculadoraCompetencias()
    # Cenário A: nota maior (5) com peso 2, nota menor (2) com peso 1. Média = 4.00
    c1 = make_competencia(1, TipoCompetencia.TECNICA, peso=2.0)
    c2 = make_competencia(2, TipoCompetencia.TECNICA, peso=1.0)

    avaliacao_a = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=5.0),
            ItemAvaliacao(competencia_id=2, nota=2.0),
        ],
    )
    res_a = calc.calcular(avaliacao_a, {1: c1, 2: c2})

    # Cenário B: nota maior (5) com peso 1, nota menor (2) com peso 2. Média = ((5*1) + (2*2)) / 3 = 3.00
    avaliacao_b = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=5.0),
            ItemAvaliacao(competencia_id=2, nota=2.0),
        ],
    )
    res_b = calc.calcular(avaliacao_b, {1: c2, 2: c1})  # Troca os pesos

    assert res_a.media_tecnica > res_b.media_tecnica
    assert res_a.media_tecnica == 4.00
    assert res_b.media_tecnica == 3.00


# 7. Absent type of competency returns 0.0.
def test_tipo_competencia_ausente():
    calc = CalculadoraCompetencias()
    c1 = make_competencia(1, TipoCompetencia.TECNICA, peso=1.0)

    avaliacao = Avaliacao(
        colaborador_id=1,
        avaliador_id=2,
        tipo=TipoAvaliacao.AVALIACAO_LIDER,
        itens=[
            ItemAvaliacao(competencia_id=1, nota=4.0),
        ],
    )

    resultado = calc.calcular(avaliacao, {1: c1})
    assert resultado.media_tecnica == 4.0
    assert resultado.media_comportamental == 0.0
    assert resultado.media_lideranca == 0.0
    assert resultado.media_organizacional == 0.0
