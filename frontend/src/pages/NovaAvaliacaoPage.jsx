import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import ErrorMessage from "../components/ui/ErrorMessage";
import Loading from "../components/ui/Loading";
import Button from "../components/ui/Button";
import AvaliacaoForm from "../features/avaliacoes/AvaliacaoForm";
import ResultadoAvaliacao from "../features/avaliacoes/ResultadoAvaliacao";
import { useAuth } from "../features/auth/useAuth";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import { criarAvaliacao, listarCompetencias } from "../features/avaliacoes/avaliacoesService";

export default function NovaAvaliacaoPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, isInitializing } = useAuth();
  
  const queryColaboradorId = searchParams.get("colaborador_id");

  // Page states
  const [colaboradores, setColaboradores] = useState([]);
  const [competencias, setCompetencias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(null);
  const [retryTrigger, setRetryTrigger] = useState(0);
  
  // Submit states
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [resultado, setResultado] = useState(null);

  const canCreateAvaliacao = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  useEffect(() => {
    if (isInitializing || !canCreateAvaliacao) return;

    const controller = new AbortController();

    const carregarDados = async () => {
      try {
        const [colabsData, compsData] = await Promise.all([
          listarColaboradores({ signal: controller.signal }),
          listarCompetencias({ signal: controller.signal })
        ]);
        setColaboradores(colabsData || []);
        setCompetencias(compsData || []);
      } catch (err) {
        if (err.name !== "AbortError" && err.code !== "ERR_CANCELED") {
          console.error("Erro ao buscar dados para avaliação:", err);
          setFetchError("Não foi possível carregar as informações necessárias para registrar a avaliação.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarDados();

    return () => {
      controller.abort();
    };
  }, [isInitializing, canCreateAvaliacao, retryTrigger]);

  const handleRetry = () => {
    setLoading(true);
    setFetchError(null);
    setRetryTrigger((prev) => prev + 1);
  };

  // Handle reload/access directly and authentication initialization
  if (isInitializing || (loading && !fetchError && canCreateAvaliacao)) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Registrar Avaliação"
          description="Aguarde enquanto os dados são carregados..."
        />
        <div className="flex justify-center py-12">
          <Loading message="Carregando colaboradores e competências..." />
        </div>
      </div>
    );
  }

  // Role Protection
  if (!canCreateAvaliacao) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Registrar Avaliação"
          description="Registrar uma nova avaliação de competências"
        />
        <div className="space-y-4">
          <ErrorMessage
            title="Acesso Negado"
            message="Você não possui permissão para registrar esta avaliação."
          />
          <div>
            <Button onClick={() => navigate("/avaliacoes")} variant="secondary">
              Voltar
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Handle Load Errors
  if (fetchError) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Registrar Avaliação"
          description="Registrar uma nova avaliação de competências"
        />
        <div className="space-y-4">
          <ErrorMessage
            title="Erro de Conexão"
            message={fetchError}
          />
          <div className="flex space-x-3">
            <Button onClick={handleRetry} variant="primary">
              Tentar Novamente
            </Button>
            <Button onClick={() => navigate("/avaliacoes")} variant="secondary">
              Voltar
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Empty data validations
  if (colaboradores.length === 0) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Registrar Avaliação"
          description="Registrar uma nova avaliação de competências"
        />
        <div className="space-y-4">
          <ErrorMessage
            title="Nenhum Colaborador Disponível"
            message="Não há colaboradores sob seu escopo de visualização disponíveis para avaliação no momento."
          />
          <div>
            <Button onClick={() => navigate("/avaliacoes")} variant="secondary">
              Voltar
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const activeCompetencias = competencias.filter((c) => c.ativo !== false);
  if (activeCompetencias.length === 0) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Registrar Avaliação"
          description="Registrar uma nova avaliação de competências"
        />
        <div className="space-y-4">
          <ErrorMessage
            title="Nenhuma Competência Ativa"
            message="Não há competências ativas cadastradas no sistema para avaliação."
          />
          <div>
            <Button onClick={() => navigate("/avaliacoes")} variant="secondary">
              Voltar
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Verify if query parameter colaborador_id is in the scope/list of loaded colaboradores
  let initialColaboradorId = "";
  if (queryColaboradorId) {
    const exists = colaboradores.some((c) => String(c.id) === String(queryColaboradorId));
    if (exists) {
      initialColaboradorId = String(queryColaboradorId);
    }
  }

  const handleSubmit = async (payload) => {
    setIsSubmitting(true);
    setSubmitError(null);
    try {
      const res = await criarAvaliacao(payload);
      setResultado(res);
      // Scroll to top to see results
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      console.error("Erro ao registrar avaliação:", err);
      const msg = err.response?.data?.message || err.response?.data?.error || "Erro ao conectar ao servidor. Verifique sua conexão e tente novamente.";
      setSubmitError(msg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    navigate("/avaliacoes");
  };

  const handleReset = () => {
    setResultado(null);
    setSubmitError(null);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Registrar Avaliação"
        description={resultado ? "Resumo dos resultados calculados pela IA" : "Registrar uma nova avaliação de competências"}
      />

      {resultado ? (
        <ResultadoAvaliacao
          resultado={resultado}
          onReset={handleReset}
        />
      ) : (
        <Card className="max-w-4xl mx-auto">
          {submitError && (
            <div className="mb-6">
              <ErrorMessage
                title="Erro ao Registrar Avaliação"
                message={submitError}
              />
            </div>
          )}
          <AvaliacaoForm
            colaboradores={colaboradores}
            competencias={activeCompetencias}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isSubmitting={isSubmitting}
            initialColaboradorId={initialColaboradorId}
            user={user}
          />
        </Card>
      )}
    </div>
  );
}
