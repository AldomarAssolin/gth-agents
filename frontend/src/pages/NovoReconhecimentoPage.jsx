import { useState, useEffect } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import { criarReconhecimento } from "../features/reconhecimentos/reconhecimentosService";
import { getReconhecimentoErrorMessage } from "../features/reconhecimentos/reconhecimentosErrors";
import ReconhecimentoForm from "../features/reconhecimentos/ReconhecimentoForm";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";

export default function NovoReconhecimentoPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const isGestor = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [colaboradores, setColaboradores] = useState([]);
  const [loading, setLoading] = useState(isGestor);
  const [loadError, setLoadError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [warningMessage, setWarningMessage] = useState("");

  const qColaboradorId = searchParams.get("colaborador_id");
  const parsedId = qColaboradorId ? Number(qColaboradorId) : null;
  const isPreselectedValid =
    parsedId &&
    Number.isInteger(parsedId) &&
    parsedId > 0 &&
    colaboradores.some((c) => c.id === parsedId);

  const finalColaboradorId = isPreselectedValid ? String(parsedId) : "";
  const lockColaborador = !!isPreselectedValid;

  useEffect(() => {
    // If not authorized, do not fetch anything
    if (!isGestor) {
      return;
    }

    const controller = new AbortController();

    const carregarColaboradores = async () => {
      try {
        setLoading(true);
        setLoadError("");
        const list = await listarColaboradores({ signal: controller.signal });
        setColaboradores(list);

        // Validate qColaboradorId ONLY after loading the list
        if (qColaboradorId) {
          const parsed = Number(qColaboradorId);
          const found = list.some((c) => c.id === parsed);

          if (!Number.isInteger(parsed) || parsed <= 0 || !found) {
            setWarningMessage(
              "O colaborador solicitado via parâmetro não foi encontrado ou está fora do seu escopo de acesso."
            );
          }
        }
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
  }, [isGestor, qColaboradorId]);

  const handleSubmit = async (formData) => {
    try {
      setIsSubmitting(true);
      setSubmitError("");
      await criarReconhecimento(formData);
      navigate("/reconhecimentos");
    } catch (err) {
      setSubmitError(getReconhecimentoErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    navigate("/reconhecimentos");
  };

  if (!isGestor) {
    return (
      <div className="space-y-6">
        <div className="flex items-center">
          <Link
            to="/reconhecimentos"
            className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
          >
            <span>&larr; Voltar para o Mural</span>
          </Link>
        </div>
        <ErrorMessage
          title="Acesso Negado"
          message="Apenas Administradores, RH e Líderes possuem permissão para registrar novos reconhecimentos."
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Link
          to="/reconhecimentos"
          className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
        >
          <span>&larr; Voltar para o Mural</span>
        </Link>
      </div>

      <PageHeader
        title="Registrar Reconhecimento"
        description="Reconheça a dedicação e os resultados de um colaborador."
      />

      {warningMessage && (
        <div className="bg-yellow-500/10 border border-yellow-500/20 text-yellow-500 text-sm px-4 py-3 rounded-lg flex items-center justify-between">
          <span>{warningMessage}</span>
          <button
            onClick={() => setWarningMessage("")}
            className="text-yellow-500 hover:text-white font-bold text-xs"
          >
            Dispensar
          </button>
        </div>
      )}

      {submitError && (
        <ErrorMessage title="Erro ao salvar reconhecimento" message={submitError} />
      )}

      {loading ? (
        <Loading message="Carregando dados necessários..." />
      ) : loadError ? (
        <div className="space-y-4">
          <ErrorMessage title="Erro de Carregamento" message={loadError} />
          <Button onClick={() => window.location.reload()} variant="primary">
            Recarregar página
          </Button>
        </div>
      ) : (
        <Card className="max-w-2xl bg-slate-800 border border-slate-700">
          <ReconhecimentoForm
            colaboradores={colaboradores}
            initialColaboradorId={finalColaboradorId}
            lockColaborador={lockColaborador}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isSubmitting={isSubmitting}
          />
        </Card>
      )}
    </div>
  );
}
