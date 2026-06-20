import { useState, useEffect } from "react";
import { useParams, Link, useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { buscarEvolucaoColaborador } from "../features/evolucao/evolucaoService";
import FeedbacksList from "../features/feedbacks/FeedbacksList";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function FeedbacksColaboradorPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const location = useLocation();
  const colaboradorId = Number(id);

  const isIdValid = Number.isInteger(colaboradorId) && colaboradorId > 0;
  const isGestor = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [colaborador, setColaborador] = useState(null);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(isIdValid);
  const [loadError, setLoadError] = useState(
    isIdValid ? "" : "Identificador de colaborador inválido."
  );
  const [successBanner, setSuccessBanner] = useState(
    location.state?.successMessage || ""
  );
  const [retryTrigger, setRetryTrigger] = useState(0);

  // Clear success banner after a few seconds
  useEffect(() => {
    if (successBanner) {
      const timer = setTimeout(() => setSuccessBanner(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [successBanner]);

  useEffect(() => {
    if (!isIdValid) return;

    const controller = new AbortController();

    const carregarFeedbacks = async () => {
      try {
        setLoading(true);
        setLoadError("");

        const data = await buscarEvolucaoColaborador(colaboradorId, {
          signal: controller.signal,
        });

        setColaborador(data.colaborador || null);
        setFeedbacks(data.feedbacks || []);
      } catch (err) {
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED") {
          const status = err.response?.status;
          if (status === 403) {
            setLoadError("Você não possui permissão para visualizar os feedbacks deste colaborador.");
          } else if (status === 404) {
            setLoadError("Colaborador não encontrado.");
          } else {
            setLoadError("Erro ao conectar à API. Por favor, tente novamente.");
          }
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarFeedbacks();

    return () => {
      controller.abort();
    };
  }, [colaboradorId, isIdValid, retryTrigger]);

  const handleRetry = () => {
    setLoading(true);
    setLoadError("");
    setRetryTrigger((prev) => prev + 1);
  };

  if (!isIdValid) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4 space-y-4">
        <ErrorMessage title="Erro de Carregamento" message={loadError} />
        <div>
          <Button onClick={() => window.history.back()} variant="secondary">
            Voltar
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Back link */}
      <div className="flex items-center">
        <Link
          to={`/colaboradores/${colaboradorId}`}
          className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
        >
          <span>&larr; Voltar para Detalhes</span>
        </Link>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <PageHeader
          title="Feedbacks do Colaborador"
          description={
            colaborador
              ? `Histórico de feedbacks estruturados para ${colaborador.nome} (${colaborador.matricula})`
              : "Histórico de feedbacks estruturados do colaborador"
          }
        />
        {isGestor && colaborador && (
          <div>
            <Link to={`/feedbacks/novo?colaborador_id=${colaboradorId}`}>
              <Button variant="primary">Registrar Feedback</Button>
            </Link>
          </div>
        )}
      </div>

      {successBanner && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/25 rounded-xl flex items-start justify-between text-emerald-400">
          <div className="flex items-start space-x-3">
            <svg
              className="h-5 w-5 mt-0.5 shrink-0"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                clipRule="evenodd"
              />
            </svg>
            <div>
              <h4 className="font-semibold text-emerald-400 text-sm">Sucesso</h4>
              <p className="text-emerald-300/85 text-xs mt-1">{successBanner}</p>
            </div>
          </div>
          <button
            onClick={() => setSuccessBanner("")}
            className="text-emerald-400 hover:text-emerald-200 transition-colors"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {loading ? (
        <Loading message="Carregando feedbacks..." className="py-12" />
      ) : loadError ? (
        <div className="space-y-4">
          <ErrorMessage title="Erro de Carregamento" message={loadError} />
          <div>
            <Button onClick={handleRetry} variant="primary">
              Tentar novamente
            </Button>
          </div>
        </div>
      ) : (
        <FeedbacksList
          feedbacks={feedbacks}
          colaboradores={colaborador ? [colaborador] : []}
          currentUser={user}
        />
      )}
    </div>
  );
}
