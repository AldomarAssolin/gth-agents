import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";

// Services & Components
import { buscarEvolucaoColaborador } from "../features/evolucao/evolucaoService";
import DadosColaboradorCard from "../features/evolucao/DadosColaboradorCard";
import PerfilTalentoCard from "../features/evolucao/PerfilTalentoCard";
import IndicadoresEvolucao from "../features/evolucao/IndicadoresEvolucao";
import ResumoCompetenciasCard from "../features/evolucao/ResumoCompetenciasCard";
import AvaliacoesTimeline from "../features/evolucao/AvaliacoesTimeline";
import AvaliacoesDetalhes from "../features/evolucao/AvaliacoesDetalhes";
import MetasResumo from "../features/evolucao/MetasResumo";
import PDISResumo from "../features/evolucao/PDISResumo";
import FeedbacksResumo from "../features/evolucao/FeedbacksResumo";
import ReconhecimentosResumo from "../features/evolucao/ReconhecimentosResumo";

export default function EvolucaoColaboradorPage() {
  const { id } = useParams();
  const colabId = Number(id);
  const isPositiveInteger = !isNaN(colabId) && Number.isInteger(colabId) && colabId > 0;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isPositiveInteger) return;

    const controller = new AbortController();

    async function fetchEvolucao() {
      // Clear previous data and errors to prevent fast-switch visual artifacts
      setData(null);
      setError(null);
      setLoading(true);

      try {
        const result = await buscarEvolucaoColaborador(colabId, { signal: controller.signal });

        if (!controller.signal.aborted) {
          setData(result);
          setLoading(false);
        }
      } catch (err) {
        if (controller.signal.aborted) {
          return;
        }

        const status = err.response?.status;
        let errorMessage = "Não foi possível carregar a evolução do colaborador.";

        if (status === 403) {
          errorMessage = "Você não possui permissão para visualizar a evolução deste colaborador.";
        } else if (status === 404) {
          errorMessage = "Colaborador não encontrado ou evolução indisponível.";
        }

        setError(errorMessage);
        setLoading(false);
      }
    }

    fetchEvolucao();

    return () => {
      controller.abort();
    };
  }, [colabId, isPositiveInteger]);

  // If ID is invalid, show the error immediately without any effect side-effects
  if (!isPositiveInteger) {
    return (
      <div className="space-y-6">
        <div className="flex items-center">
          <Link
            to="/colaboradores"
            className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
          >
            <span>&larr; Voltar para Colaboradores</span>
          </Link>
        </div>

        <PageHeader
          title="Evolução do Colaborador"
          description="Acompanhamento e evolução de competências"
        />

        <ErrorMessage
          title="Erro de Carregamento"
          message="Identificador de colaborador inválido."
          className="my-6"
        />
      </div>
    );
  }

  const colabName = data?.colaborador?.nome || "Colaborador";

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Link
          to={`/colaboradores/${colabId}`}
          className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
        >
          <span>&larr; Voltar para Detalhes</span>
        </Link>
      </div>

      <PageHeader
        title="Evolução do Colaborador"
        description={`Acompanhamento e evolução de competências para ${colabName}`}
      />

      {loading && <Loading message="Carregando histórico de evolução..." className="py-24" />}

      {!loading && error && (
        <ErrorMessage
          title="Erro de Carregamento"
          message={error}
          className="my-6"
        />
      )}

      {!loading && !error && data && (
        <div className="grid grid-cols-1 gap-6">
          {/* Header Card with Basic Info */}
          <DadosColaboradorCard colaborador={data.colaborador} />

          {/* Competency Ratings Averages */}
          <ResumoCompetenciasCard indicadores={data.indicadores} />

          {/* Talent Profile details */}
          <PerfilTalentoCard perfilAtual={data.perfil_atual} />

          {/* General Evolution Counters */}
          <IndicadoresEvolucao indicadores={data.indicadores} />

          {/* Split lists: Details/Timeline on Left, Goals/PDIs/Recognitions on Right */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              {/* Chronological summarized timeline */}
              <AvaliacoesTimeline ultimasAvaliacoes={data.ultimas_avaliacoes} />

              {/* Detailed scores / items table */}
              <AvaliacoesDetalhes avaliacoes={data.avaliacoes} />

              {/* Feedbacks list */}
              <FeedbacksResumo feedbacks={data.feedbacks} />
            </div>

            <div className="space-y-6">
              {/* Metas/Goals */}
              <MetasResumo metas={data.metas} />

              {/* PDIs */}
              <PDISResumo pdis={data.pdis} />

              {/* Conquistas/Recognitions */}
              <ReconhecimentosResumo reconhecimentos={data.reconhecimentos} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
