import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import { criarMeta } from "../features/metas/metasService";
import { getMetaErrorMessage } from "../features/metas/metasErrors";
import MetaForm from "../features/metas/MetaForm";
import StatusMetaBadge from "../features/metas/StatusMetaBadge";
import PrioridadeMetaBadge from "../features/metas/PrioridadeMetaBadge";
import { formatarData } from "../features/metas/metasFormatters";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function NovaMetaPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const isPermitted = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [colaboradores, setColaboradores] = useState([]);
  const [loading, setLoading] = useState(isPermitted);
  const [loadError, setLoadError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [createdMeta, setCreatedMeta] = useState(null);

  // Parse parameters from query string
  const qColaboradorId = searchParams.get("colaborador_id");
  let preselectedId = "";

  if (qColaboradorId) {
    const parsed = Number(qColaboradorId);
    if (Number.isInteger(parsed) && parsed > 0) {
      preselectedId = String(parsed);
    }
  }

  useEffect(() => {
    if (!isPermitted) return;

    const controller = new AbortController();

    const carregarColaboradores = async () => {
      try {
        setLoading(true);
        setLoadError("");
        const list = await listarColaboradores({ signal: controller.signal });
        setColaboradores(list);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setLoadError("Erro ao carregar lista de colaboradores.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarColaboradores();

    return () => {
      controller.abort();
    };
  }, [isPermitted]);

  if (!isPermitted) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4">
        <ErrorMessage
          title="Acesso Negado"
          message="Você não possui permissão para acessar esta página de criação de metas."
        />
        <div className="mt-4">
          <Button onClick={() => navigate("/metas")} variant="secondary">
            Voltar para Metas
          </Button>
        </div>
      </div>
    );
  }

  if (loading) {
    return <Loading message="Carregando dados necessários..." />;
  }

  if (loadError) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4 space-y-4">
        <ErrorMessage title="Erro ao carregar página" message={loadError} />
        <div>
          <Button onClick={() => navigate("/metas")} variant="secondary">
            Voltar
          </Button>
        </div>
      </div>
    );
  }

  // Validate preselected ID matches one of the accessible colaboradores
  const hasPreselectedValue = preselectedId !== "";
  const isPreselectedIdValid =
    hasPreselectedValue && colaboradores.some((c) => c.id === Number(preselectedId));

  const finalColaboradorId = isPreselectedIdValid ? preselectedId : "";

  const handleSubmit = async (formData) => {
    try {
      setIsSubmitting(true);
      setSubmitError("");

      // criado_por_id is forced from user.id for security (mitigating backend risk)
      const payload = {
        ...formData,
        criado_por_id: user.id,
      };

      const result = await criarMeta(payload);
      setCreatedMeta(result);
    } catch (err) {
      setSubmitError(getMetaErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCreateAnother = () => {
    setCreatedMeta(null);
    setSubmitError("");
  };

  if (createdMeta) {
    const colName =
      colaboradores.find((c) => c.id === createdMeta.colaborador_id)?.nome ||
      `Colaborador #${createdMeta.colaborador_id}`;

    return (
      <div className="max-w-2xl mx-auto py-8 px-4">
        <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-6 shadow-xl space-y-6">
          <div className="flex items-center space-x-3 text-emerald-400">
            <svg
              className="w-8 h-8 shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h2 className="text-xl font-bold text-white">Meta Criada com Sucesso!</h2>
          </div>

          <div className="bg-slate-900/50 border border-slate-700/40 rounded-lg p-5 space-y-4">
            <div>
              <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Colaborador
              </span>
              <span className="text-white font-medium">{colName}</span>
            </div>

            <div>
              <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Título
              </span>
              <span className="text-white font-semibold text-lg">{createdMeta.titulo}</span>
            </div>

            <div>
              <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Descrição
              </span>
              <p className="text-slate-300 text-sm mt-1">{createdMeta.descricao}</p>
            </div>

            {createdMeta.indicador && (
              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Indicador de Sucesso
                </span>
                <span className="text-slate-300 text-sm mt-1 italic block">
                  {createdMeta.indicador}
                </span>
              </div>
            )}

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 pt-2 border-t border-slate-800">
              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Prazo
                </span>
                <span className="text-slate-200 text-sm">{formatarData(createdMeta.prazo)}</span>
              </div>

              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Prioridade
                </span>
                <div className="mt-1">
                  <PrioridadeMetaBadge prioridade={createdMeta.prioridade} />
                </div>
              </div>

              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Status
                </span>
                <div className="mt-1">
                  <StatusMetaBadge status={createdMeta.status} />
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-end gap-3 pt-4 border-t border-slate-700">
            <Button onClick={handleCreateAnother} variant="secondary">
              Criar Outra Meta
            </Button>
            <Button
              onClick={() => navigate(`/colaboradores/${createdMeta.colaborador_id}/metas`)}
              variant="primary"
            >
              Ver Metas do Colaborador
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-6 shadow-xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Criar Nova Meta</h1>
          <p className="text-slate-400 text-sm mt-1">
            Preencha os campos abaixo para definir uma nova meta de desempenho para o colaborador.
          </p>
        </div>

        {submitError && <ErrorMessage title="Erro de Validação/Servidor" message={submitError} />}

        <MetaForm
          colaboradores={colaboradores}
          initialColaboradorId={finalColaboradorId}
          lockColaborador={isPreselectedIdValid}
          onSubmit={handleSubmit}
          onCancel={() => navigate("/metas")}
          isSubmitting={isSubmitting}
        />
      </div>
    </div>
  );
}
