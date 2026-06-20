import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import { criarFeedback } from "../features/feedbacks/feedbacksService";
import { getFeedbackErrorMessage } from "../features/feedbacks/feedbacksErrors";
import FeedbackForm from "../features/feedbacks/FeedbackForm";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function NovoFeedbackPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const isPermitted = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);
  const userHasNumericId = typeof user?.id === "number";

  const [colaboradores, setColaboradores] = useState([]);
  const [loading, setLoading] = useState(isPermitted && userHasNumericId);
  const [loadError, setLoadError] = useState(
    !isPermitted ? "" : (userHasNumericId ? "" : "Identificador do usuário autenticado é inválido ou não numérico.")
  );
  const [submitError, setSubmitError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Parse query parameters
  const qColaboradorId = searchParams.get("colaborador_id");
  let preselectedId = "";
  if (qColaboradorId) {
    const parsed = Number(qColaboradorId);
    if (Number.isInteger(parsed) && parsed > 0) {
      preselectedId = String(parsed);
    }
  }

  useEffect(() => {
    if (!isPermitted || !userHasNumericId) return;

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
  }, [isPermitted, user, userHasNumericId]);

  if (!isPermitted) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4">
        <ErrorMessage
          title="Acesso Negado"
          message="Você não possui permissão para acessar esta página de criação de Feedback."
        />
        <div className="mt-4">
          <Button onClick={() => navigate("/feedbacks")} variant="secondary">
            Voltar para Feedbacks
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
          <Button onClick={() => navigate("/feedbacks")} variant="secondary">
            Voltar
          </Button>
        </div>
      </div>
    );
  }

  // Preselected validation (must exist in loaded colaboradores)
  const isPreselectedValid =
    preselectedId !== "" && colaboradores.some((c) => c.id === Number(preselectedId));
  const finalColaboradorId = isPreselectedValid ? preselectedId : "";

  const handleSubmit = async (formData) => {
    try {
      setIsSubmitting(true);
      setSubmitError("");
      setSuccessMessage("");

      // Double-check numeric user.id before submit
      if (typeof user?.id !== "number") {
        throw new Error("Erro de Segurança: ID do autor inválido.");
      }

      const payload = {
        ...formData,
        autor_id: user.id,
      };

      await criarFeedback(payload);

      setSuccessMessage("Feedback registrado com sucesso!");

      // Automatic redirect after 1.5 seconds
      setTimeout(() => {
        navigate(`/colaboradores/${formData.colaborador_id}/feedbacks`, {
          state: { successMessage: "Feedback registrado com sucesso!" },
        });
      }, 1500);
    } catch (err) {
      setSubmitError(getFeedbackErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-6 shadow-xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Registrar Feedback</h1>
          <p className="text-slate-400 text-sm mt-1">
            Insira o feedback estruturado para o colaborador selecionado.
          </p>
        </div>

        {submitError && (
          <ErrorMessage title="Erro ao salvar feedback" message={submitError} />
        )}

        {successMessage && (
          <div className="p-4 bg-emerald-500/10 border border-emerald-500/25 rounded-xl flex items-start space-x-3 text-emerald-400">
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
              <p className="text-emerald-300/85 text-xs mt-1">
                {successMessage} Redirecionando...
              </p>
            </div>
          </div>
        )}

        <FeedbackForm
          colaboradores={colaboradores}
          initialColaboradorId={finalColaboradorId}
          lockColaborador={isPreselectedValid}
          onSubmit={handleSubmit}
          onCancel={() => navigate("/feedbacks")}
          isSubmitting={isSubmitting || !!successMessage}
        />
      </div>
    </div>
  );
}
