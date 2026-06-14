import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { buscarPDI, atualizarPDI } from "../features/pdis/pdisService";
import { getPDIErrorMessage } from "../features/pdis/pdisErrors";
import PDIForm from "../features/pdis/PDIForm";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function EditarPDIPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const isPermitted = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);
  const pdiId = Number(id);
  const isIdValido = Number.isInteger(pdiId) && pdiId > 0;

  const [pdi, setPdi] = useState(null);
  const [loading, setLoading] = useState(isPermitted && isIdValido);
  const [loadError, setLoadError] = useState(isIdValido ? "" : "Identificador de PDI inválido.");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!isPermitted || !isIdValido) return;

    const controller = new AbortController();

    const carregarPDI = async () => {
      try {
        setLoading(true);
        setLoadError("");
        setSubmitError("");
        setPdi(null);
        const data = await buscarPDI(pdiId, { signal: controller.signal });
        
        if (controller.signal.aborted) return;

        if (data.status === "CONCLUIDO" || data.status === "CANCELADO") {
          setLoadError(`Este PDI já está ${data.status.toLowerCase()} e não pode ser editado.`);
        } else {
          setPdi(data);
        }
      } catch (err) {
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED" && !controller.signal.aborted) {
          setLoadError(getPDIErrorMessage(err));
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarPDI();

    return () => {
      controller.abort();
    };
  }, [pdiId, isPermitted, isIdValido]);

  if (!isPermitted) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4">
        <ErrorMessage
          title="Acesso Negado"
          message="Você não possui permissão para acessar esta página de edição de PDI."
        />
        <div className="mt-4">
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar
          </Button>
        </div>
      </div>
    );
  }

  if (!isIdValido) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4">
        <ErrorMessage title="ID Inválido" message="Identificador de PDI inválido." />
        <div className="mt-4">
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar para lista
          </Button>
        </div>
      </div>
    );
  }

  if (loading) {
    return <Loading message="Carregando dados do PDI..." />;
  }

  if (loadError) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4 space-y-4">
        <ErrorMessage title="Erro ao carregar PDI" message={loadError} />
        <div>
          <Button onClick={() => navigate(`/pdis/${pdiId}`)} variant="secondary">
            Voltar para Detalhes
          </Button>
        </div>
      </div>
    );
  }

  const handleSubmit = async (formData) => {
    try {
      setIsSubmitting(true);
      setSubmitError("");
      await atualizarPDI(pdiId, formData);
      navigate(`/pdis/${pdiId}`); // Screen synchronization via redirect to details page
    } catch (err) {
      setSubmitError(getPDIErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-6 shadow-xl space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Editar PDI</h1>
          <p className="text-slate-400 text-sm mt-1">
            Modifique o título, descrição ou datas planejadas para este plano de desenvolvimento.
          </p>
        </div>

        {submitError && <ErrorMessage title="Erro ao salvar alterações" message={submitError} />}

        {pdi && (
          <PDIForm
            isEdit={true}
            initialData={pdi}
            onSubmit={handleSubmit}
            onCancel={() => navigate(`/pdis/${pdiId}`)}
            isSubmitting={isSubmitting}
          />
        )}
      </div>
    </div>
  );
}
