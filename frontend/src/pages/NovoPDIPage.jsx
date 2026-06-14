import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import { criarPDI } from "../features/pdis/pdisService";
import { getPDIErrorMessage } from "../features/pdis/pdisErrors";
import PDIForm from "../features/pdis/PDIForm";
import StatusPDIBadge from "../features/pdis/StatusPDIBadge";
import { formatarData, traduzirOrigemPDI } from "../features/pdis/pdisFormatters";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function NovoPDIPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const isPermitted = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [colaboradores, setColaboradores] = useState([]);
  const [loading, setLoading] = useState(isPermitted);
  const [loadError, setLoadError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [createdPdi, setCreatedPdi] = useState(null);

  // Parse collaborator_id query param
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
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED") {
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
          message="Você não possui permissão para acessar esta página de criação de PDI."
        />
        <div className="mt-4">
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar para PDIs
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
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar
          </Button>
        </div>
      </div>
    );
  }

  // Check if preselected matches an accessible collaborator
  const isPreselectedValid =
    preselectedId !== "" && colaboradores.some((c) => c.id === Number(preselectedId));
  const finalColaboradorId = isPreselectedValid ? preselectedId : "";

  const handleSubmit = async (formData) => {
    try {
      setIsSubmitting(true);
      setSubmitError("");

      const result = await criarPDI(formData);
      setCreatedPdi(result);
    } catch (err) {
      setSubmitError(getPDIErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCreateAnother = () => {
    setCreatedPdi(null);
    setSubmitError("");
  };

  if (createdPdi) {
    const colName =
      colaboradores.find((c) => c.id === createdPdi.colaborador_id)?.nome ||
      `Colaborador #${createdPdi.colaborador_id}`;

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
            <h2 className="text-xl font-bold text-white">PDI Criado com Sucesso!</h2>
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
              <span className="text-white font-semibold text-lg">{createdPdi.titulo}</span>
            </div>

            <div>
              <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Descrição / Objetivos
              </span>
              <p className="text-slate-300 text-sm mt-1">{createdPdi.descricao}</p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2 border-t border-slate-800">
              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Início
                </span>
                <span className="text-slate-200 text-sm">{formatarData(createdPdi.data_inicio)}</span>
              </div>

              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Término
                </span>
                <span className="text-slate-200 text-sm">{formatarData(createdPdi.data_fim)}</span>
              </div>

              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Origem
                </span>
                <span className="text-slate-200 text-sm block mt-1">{traduzirOrigemPDI(createdPdi.origem)}</span>
              </div>

              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Status
                </span>
                <div className="mt-1">
                  <StatusPDIBadge status={createdPdi.status} />
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-end gap-3 pt-4 border-t border-slate-700">
            <Button onClick={handleCreateAnother} variant="secondary">
              Criar Outro PDI
            </Button>
            <Button
              onClick={() => navigate(`/pdis/${createdPdi.id}`)}
              variant="primary"
            >
              Ver Detalhes do PDI
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
          <h1 className="text-2xl font-bold text-white">Criar Novo PDI</h1>
          <p className="text-slate-400 text-sm mt-1">
            Preencha as informações para estabelecer o Plano de Desenvolvimento Individual do colaborador.
          </p>
        </div>

        {submitError && <ErrorMessage title="Erro de Validação/Servidor" message={submitError} />}

        <PDIForm
          colaboradores={colaboradores}
          initialColaboradorId={finalColaboradorId}
          lockColaborador={isPreselectedValid}
          onSubmit={handleSubmit}
          onCancel={() => navigate("/pdis")}
          isSubmitting={isSubmitting}
        />
      </div>
    </div>
  );
}
