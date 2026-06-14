import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { buscarColaboradorPorId } from "../features/colaboradores/colaboradoresService";
import {
  listarReconhecimentosPorColaborador,
  cancelarReconhecimento,
} from "../features/reconhecimentos/reconhecimentosService";
import { getReconhecimentoErrorMessage } from "../features/reconhecimentos/reconhecimentosErrors";
import ReconhecimentosList from "../features/reconhecimentos/ReconhecimentosList";
import CancelarReconhecimentoDialog from "../features/reconhecimentos/CancelarReconhecimentoDialog";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function ReconhecimentosColaboradorPage() {
  const { id } = useParams();
  const colaboradorId = Number(id);
  const idValido = Number.isInteger(colaboradorId) && colaboradorId > 0;
  const { user } = useAuth();
  const isGestor = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [colaborador, setColaborador] = useState(null);
  const [reconhecimentos, setReconhecimentos] = useState([]);
  const [loading, setLoading] = useState(idValido);
  const [loadError, setLoadError] = useState(
    idValido ? "" : "Identificador do colaborador inválido."
  );

  // Cancel states
  const [cancelError, setCancelError] = useState("");
  const [isCancelling, setIsCancelling] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [reconhecimentoToCancel, setReconhecimentoToCancel] = useState(null);

  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!idValido) return;

    const controller = new AbortController();

    const carregarDados = async () => {
      try {
        setLoading(true);
        setLoadError("");

        const [colabData, reconhecimentosData] = await Promise.all([
          buscarColaboradorPorId(colaboradorId, { signal: controller.signal }),
          listarReconhecimentosPorColaborador(colaboradorId, { signal: controller.signal }),
        ]);

        setColaborador(colabData);
        setReconhecimentos(reconhecimentosData);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setLoadError(getReconhecimentoErrorMessage(err));
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
  }, [colaboradorId, idValido, retryTrigger]);

  const handleRetry = () => {
    setRetryTrigger((prev) => prev + 1);
  };

  const handleOpenCancelDialog = (reconhecimento) => {
    setCancelError("");
    setReconhecimentoToCancel(reconhecimento);
    setDialogOpen(true);
  };

  const handleCloseCancelDialog = () => {
    if (isCancelling) return;
    setDialogOpen(false);
    setReconhecimentoToCancel(null);
    setCancelError("");
  };

  const handleConfirmCancel = async (motivo) => {
    if (!reconhecimentoToCancel) return;

    try {
      setIsCancelling(true);
      setCancelError("");

      const updated = await cancelarReconhecimento(reconhecimentoToCancel.id, motivo);

      setReconhecimentos((prev) =>
        prev.map((rec) => (rec.id === updated.id ? updated : rec))
      );

      setDialogOpen(false);
      setReconhecimentoToCancel(null);
    } catch (err) {
      setCancelError(getReconhecimentoErrorMessage(err));
    } finally {
      setIsCancelling(false);
    }
  };

  const actions = isGestor && colaborador ? (
    <Link to={`/reconhecimentos/novo?colaborador_id=${colaborador.id}`}>
      <Button variant="primary">Registrar Reconhecimento</Button>
    </Link>
  ) : null;

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Link
          to={`/colaboradores/${colaboradorId}`}
          className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
        >
          <span>&larr; Voltar para Detalhes do Colaborador</span>
        </Link>
      </div>

      {cancelError && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm px-4 py-3 rounded-lg flex items-center justify-between">
          <span>{cancelError}</span>
          <button
            onClick={() => setCancelError("")}
            className="text-red-400 hover:text-white font-bold text-xs"
          >
            Fechar
          </button>
        </div>
      )}

      {loading ? (
        <Loading message="Carregando reconhecimentos do colaborador..." />
      ) : loadError ? (
        <div className="space-y-4">
          <ErrorMessage title="Erro de Carregamento" message={loadError} />
          <Button onClick={handleRetry} variant="primary">
            Tentar novamente
          </Button>
        </div>
      ) : (
        <>
          <PageHeader
            title={`Reconhecimentos: ${colaborador?.nome}`}
            description="Histórico de agradecimentos e celebrações registrados para este colaborador."
            actions={actions}
          />

          <ReconhecimentosList
            reconhecimentos={reconhecimentos}
            colaboradores={colaborador ? [colaborador] : []}
            currentUser={user}
            onCancelar={handleOpenCancelDialog}
            showColaboradorFilter={false}
          />
        </>
      )}

      {dialogOpen && (
        <CancelarReconhecimentoDialog
          isOpen={dialogOpen}
          onClose={handleCloseCancelDialog}
          onConfirm={handleConfirmCancel}
          isSubmitting={isCancelling}
          apiError={cancelError}
        />
      )}
    </div>
  );
}
