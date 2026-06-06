import pytest
from domain.services.calculadora_competencias import ResultadoCompetencias
from domain.services.classificador_talento import ClassificadorTalento
from domain.enums.classificacao_talento import ClassificacaoTalento


# 8. Média maior ou igual a 4 retorna nível ALTO.
# 9. Média entre 3 e 3.99 retorna nível MEDIO.
# 10. Média entre 0.1 e 2.99 retorna nível BAIXO.
# 11. Média 0 retorna nível NAO_AVALIADO.
def test_niveis_textuais_medias():
    classificador = ClassificadorTalento()

    # ALTO
    assert classificador._nivel(4.0) == "ALTO"
    assert classificador._nivel(4.5) == "ALTO"

    # MEDIO
    assert classificador._nivel(3.0) == "MEDIO"
    assert classificador._nivel(3.99) == "MEDIO"

    # BAIXO
    assert classificador._nivel(0.1) == "BAIXO"
    assert classificador._nivel(2.99) == "BAIXO"

    # NAO_AVALIADO
    assert classificador._nivel(0.0) == "NAO_AVALIADO"


# 12. Classifica corretamente ALTA_PERFORMANCE.
def test_classifica_alta_performance():
    classificador = ClassificadorTalento()

    # Com liderança
    res1 = ResultadoCompetencias(
        media_tecnica=4.5,
        media_comportamental=4.0,
        media_lideranca=4.0,
        media_organizacional=4.0,
        media_geral=4.12,
    )
    perfil1 = classificador.classificar(1, res1)
    assert perfil1.classificacao == ClassificacaoTalento.ALTA_PERFORMANCE

    # Sem liderança avaliada
    res2 = ResultadoCompetencias(
        media_tecnica=4.5,
        media_comportamental=4.0,
        media_lideranca=0.0,
        media_organizacional=4.0,
        media_geral=4.12,
    )
    perfil2 = classificador.classificar(1, res2)
    assert perfil2.classificacao == ClassificacaoTalento.ALTA_PERFORMANCE


# 13. Classifica corretamente POTENCIAL_LIDER.
def test_classifica_potencial_lider():
    classificador = ClassificadorTalento()

    # técnico >= 3, comportamental >= 4, lideranca >= 4
    res1 = ResultadoCompetencias(
        media_tecnica=3.5,
        media_comportamental=4.2,
        media_lideranca=4.0,
        media_organizacional=3.0,
        media_geral=3.68,
    )
    perfil1 = classificador.classificar(1, res1)
    assert perfil1.classificacao == ClassificacaoTalento.POTENCIAL_LIDER

    # técnico >= 4, lideranca >= 4 (comportamental < 4)
    res2 = ResultadoCompetencias(
        media_tecnica=4.5,
        media_comportamental=3.5,
        media_lideranca=4.0,
        media_organizacional=3.0,
        media_geral=3.75,
    )
    perfil2 = classificador.classificar(1, res2)
    assert perfil2.classificacao == ClassificacaoTalento.POTENCIAL_LIDER


# 14. Classifica corretamente ESPECIALISTA_TECNICO.
def test_classifica_especialista_tecnico():
    classificador = ClassificadorTalento()

    # técnico >= 4, comportamental < 4 (liderança não avaliada ou < 4)
    res1 = ResultadoCompetencias(
        media_tecnica=4.2,
        media_comportamental=3.5,
        media_lideranca=0.0,
        media_organizacional=3.0,
        media_geral=3.57,
    )
    perfil1 = classificador.classificar(1, res1)
    assert perfil1.classificacao == ClassificacaoTalento.ESPECIALISTA_TECNICO

    # técnico >= 4, lideranca < 4
    res2 = ResultadoCompetencias(
        media_tecnica=4.2,
        media_comportamental=4.2,
        media_lideranca=2.5,
        media_organizacional=3.0,
        media_geral=3.48,
    )
    perfil2 = classificador.classificar(1, res2)
    assert perfil2.classificacao == ClassificacaoTalento.ESPECIALISTA_TECNICO


# 15. Classifica corretamente TALENTO_EM_DESENVOLVIMENTO.
def test_classifica_talento_em_desenvolvimento():
    classificador = ClassificadorTalento()

    # media_geral >= 3, tecnico >= 3 ou comportamental >= 3
    res1 = ResultadoCompetencias(
        media_tecnica=3.2,
        media_comportamental=2.8,
        media_lideranca=0.0,
        media_organizacional=3.0,
        media_geral=3.0,
    )
    perfil1 = classificador.classificar(1, res1)
    assert perfil1.classificacao == ClassificacaoTalento.TALENTO_EM_DESENVOLVIMENTO


# 16. Classifica corretamente NECESSITA_DESENVOLVIMENTO.
def test_classifica_necessita_desenvolvimento():
    classificador = ClassificadorTalento()

    # media_geral < 3
    res1 = ResultadoCompetencias(
        media_tecnica=3.5,
        media_comportamental=3.5,
        media_lideranca=0.0,
        media_organizacional=1.0,
        media_geral=2.6,
    )
    perfil1 = classificador.classificar(1, res1)
    assert perfil1.classificacao == ClassificacaoTalento.NECESSITA_DESENVOLVIMENTO

    # tecnico < 3 e comportamental < 3
    res2 = ResultadoCompetencias(
        media_tecnica=2.5,
        media_comportamental=2.5,
        media_lideranca=4.0,
        media_organizacional=4.0,
        media_geral=3.25,
    )
    perfil2 = classificador.classificar(1, res2)
    assert perfil2.classificacao == ClassificacaoTalento.NECESSITA_DESENVOLVIMENTO


# 17. Não gera ponto de melhoria para tipo de competência não avaliado.
def test_nao_gera_melhoria_para_nao_avaliado():
    classificador = ClassificadorTalento()

    res = ResultadoCompetencias(
        media_tecnica=4.0,
        media_comportamental=4.0,
        media_lideranca=0.0,  # Não avaliado
        media_organizacional=0.0,  # Não avaliado
        media_geral=4.0,
    )
    perfil = classificador.classificar(1, res)
    assert not any("liderança" in m.lower() for m in perfil.pontos_melhoria)
    assert not any("organizacional" in m.lower() for m in perfil.pontos_melhoria)
    assert not any("aderência" in m.lower() for m in perfil.pontos_melhoria)


# 18. Gera pontos fortes coerentes com médias altas.
def test_gera_pontos_fortes_coerentes():
    classificador = ClassificadorTalento()

    res = ResultadoCompetencias(
        media_tecnica=4.5,
        media_comportamental=4.2,
        media_lideranca=4.0,
        media_organizacional=4.8,
        media_geral=4.38,
    )
    perfil = classificador.classificar(1, res)
    assert "Boa competência técnica." in perfil.pontos_fortes
    assert "Bom comportamento organizacional." in perfil.pontos_fortes
    assert "Boa capacidade de liderança." in perfil.pontos_fortes
    assert "Boa aderência aos valores e práticas organizacionais." in perfil.pontos_fortes


# 19. Gera recomendações coerentes com a classificação.
def test_gera_recomendacoes_coerentes():
    classificador = ClassificadorTalento()

    # ALTA_PERFORMANCE
    perfil_ap = classificador.classificar(1, ResultadoCompetencias(4.5, 4.5, 4.5, 4.0, 4.38))
    assert "Manter acompanhamento e oferecer desafios maiores." in perfil_ap.recomendacoes
    assert "Considerar para projetos estratégicos ou mentoria." in perfil_ap.recomendacoes

    # POTENCIAL_LIDER
    perfil_pl = classificador.classificar(1, ResultadoCompetencias(4.5, 3.5, 4.5, 3.0, 3.88))
    assert "Incluir em atividades de apoio à liderança." in perfil_pl.recomendacoes

    # ESPECIALISTA_TECNICO
    perfil_et = classificador.classificar(1, ResultadoCompetencias(4.5, 3.5, 2.5, 3.0, 3.38))
    assert "Utilizar como referência técnica." in perfil_et.recomendacoes

    # TALENTO_EM_DESENVOLVIMENTO
    perfil_td = classificador.classificar(1, ResultadoCompetencias(3.5, 3.5, 0.0, 3.0, 3.33))
    assert "Criar plano de desenvolvimento individual." in perfil_td.recomendacoes

    # NECESSITA_DESENVOLVIMENTO
    perfil_nd = classificador.classificar(1, ResultadoCompetencias(2.5, 2.5, 0.0, 3.0, 2.67))
    assert "Priorizar treinamento e acompanhamento próximo." in perfil_nd.recomendacoes
