import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import { buscarEvolucaoColaborador } from "../features/evolucao/evolucaoService";
import FeedbacksList from "../features/feedbacks/FeedbacksList";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";
import Select from "../components/ui/Select";
import Card from "../components/ui/Card";

export default function FeedbacksPage() {
  const { user } = useAuth();
  const isGestor = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [colaboradores, setColaboradores] = useState([]);
  const [selectedColaboradorId, setSelectedColaboradorId] = useState("");
  const [feedbacks, setFeedbacks] = useState([]);

  // Error separation
  const [loadError, setLoadError] = useState("");
  const [feedbacksError, setFeedbacksError] = useState("");

  // Loading states
  const [loadingColaboradores, setLoadingColaboradores] = useState(true);
  const [loadingFeedbacks, setLoadingFeedbacks] = useState(false);

  // Load colaboradores on mount
  useEffect(() => {
    const controller = new AbortController();

    async function loadInitialData() {
      try {
        setLoadingColaboradores(true);
        setLoadError("");
        const list = await listarColaboradores({ signal: controller.signal });
        setColaboradores(list);

        // If user is a COLABORADOR, they can only see their own.
        // If there's exactly one collaborator returned in the list (e.g. self-only), auto-select it.
        if (list.length === 1) {
          setSelectedColaboradorId(String(list[0].id));
        }
      } catch (err) {
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED") {
          setLoadError("Não foi possível carregar a lista de colaboradores.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoadingColaboradores(false);
        }
      }
    }

    loadInitialData();

    return () => {
      controller.abort();
    };
  }, []);

  // Fetch feedbacks when a collaborator is selected
  useEffect(() => {
    if (!selectedColaboradorId) return;

    const controller = new AbortController();

    async function fetchFeedbacks() {
      try {
        setLoadingFeedbacks(true);
        setFeedbacksError("");
        const data = await buscarEvolucaoColaborador(Number(selectedColaboradorId), {
          signal: controller.signal,
        });
        setFeedbacks(data.feedbacks || []);
      } catch (err) {
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED") {
          const status = err.response?.status;
          if (status === 403) {
            setFeedbacksError(
              "Você não possui permissão para visualizar os feedbacks deste colaborador."
            );
          } else if (status === 404) {
            setFeedbacksError("Colaborador não encontrado.");
          } else {
            setFeedbacksError("Erro ao conectar ao servidor. Tente novamente.");
          }
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoadingFeedbacks(false);
        }
      }
    }

    fetchFeedbacks();

    return () => {
      controller.abort();
    };
  }, [selectedColaboradorId]);

  if (loadingColaboradores) {
    return <Loading message="Carregando colaboradores..." className="py-12" />;
  }

  if (loadError) {
    return (
      <div className="space-y-4">
        <ErrorMessage title="Erro de Carregamento" message={loadError} />
        <div>
          <Button onClick={() => window.location.reload()} variant="primary">
            Tentar novamente
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <PageHeader
          title="Feedbacks"
          description="Central de feedbacks estruturados dos colaboradores"
        />
        {isGestor && selectedColaboradorId && !feedbacksError && (
          <div>
            <Link to={`/feedbacks/novo?colaborador_id=${selectedColaboradorId}`}>
              <Button variant="primary">Registrar Feedback</Button>
            </Link>
          </div>
        )}
      </div>

      {/* Collaborator Selector */}
      <Card className="bg-slate-800 border border-slate-700/60 shadow-md">
        <div className="max-w-md">
          <Select
            id="seletor-colaborador"
            label="Selecione um Colaborador"
            value={selectedColaboradorId}
            onChange={(e) => {
              const val = e.target.value;
              setSelectedColaboradorId(val);
              if (!val) {
                setFeedbacks([]);
                setFeedbacksError("");
              }
            }}
            options={[
              { label: "Selecione um colaborador...", value: "" },
              ...colaboradores.map((c) => ({
                label: `${c.nome} (${c.matricula || c.id})`,
                value: String(c.id),
              })),
            ]}
          />
        </div>
        <p className="text-slate-500 text-xs mt-3">
          Nota: O sistema não disponibiliza uma listagem global unificada. A consulta deve ser feita individualmente por colaborador.
        </p>
      </Card>

      {/* Feedbacks Display Area */}
      {!selectedColaboradorId ? (
        <Card className="bg-slate-900 border-slate-800 py-12 text-center">
          <p className="text-slate-400 text-sm">
            Selecione um colaborador acima para visualizar os feedbacks registrados.
          </p>
        </Card>
      ) : loadingFeedbacks ? (
        <Loading message="Buscando feedbacks do colaborador..." className="py-12" />
      ) : feedbacksError ? (
        <ErrorMessage title="Erro ao carregar feedbacks" message={feedbacksError} />
      ) : (
        <FeedbacksList
          feedbacks={feedbacks}
          colaboradores={colaboradores}
          currentUser={user}
        />
      )}
    </div>
  );
}
