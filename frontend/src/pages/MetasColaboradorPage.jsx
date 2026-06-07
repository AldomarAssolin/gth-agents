import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { buscarColaboradorPorId } from "../features/colaboradores/colaboradoresService";
import MetasColaboradorView from "../features/metas/MetasColaboradorView";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function MetasColaboradorPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const parsedId = Number(id);
  const isIdValido = Number.isInteger(parsedId) && parsedId > 0;

  const [colaborador, setColaborador] = useState(null);
  const [loading, setLoading] = useState(isIdValido);
  const [error, setError] = useState(isIdValido ? "" : "Identificador de colaborador inválido.");

  const canCreateMeta = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  useEffect(() => {
    if (!isIdValido) return;

    const controller = new AbortController();

    const carregarColaborador = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await buscarColaboradorPorId(parsedId, {
          signal: controller.signal,
        });
        setColaborador(data);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setError("Não foi possível carregar os detalhes do colaborador.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarColaborador();

    return () => {
      controller.abort();
    };
  }, [parsedId, isIdValido]);

  if (!isIdValido) {
    return (
      <div className="max-w-7xl mx-auto py-8 px-4">
        <ErrorMessage title="Erro de Validação" message={error} />
        <div className="mt-4">
          <Button onClick={() => navigate("/metas")} variant="secondary">
            Voltar para Metas
          </Button>
        </div>
      </div>
    );
  }

  if (loading) {
    return <Loading message="Carregando dados do colaborador..." />;
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto py-8 px-4 space-y-4">
        <ErrorMessage title="Erro de Carregamento" message={error} />
        <div>
          <Button onClick={() => navigate("/metas")} variant="secondary">
            Voltar
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-sm text-slate-400">
            <span className="hover:text-white cursor-pointer" onClick={() => navigate("/metas")}>
              Metas
            </span>
            <span>&gt;</span>
            <span className="text-slate-300">Metas do Colaborador</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">
            Metas de {colaborador?.nome || `Colaborador #${id}`}
          </h1>
          <p className="text-sm text-slate-400 mt-0.5">
            Matrícula: {colaborador?.matricula || "Não informada"} | Setor: {colaborador?.setor?.nome || "Não informado"}
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <Button onClick={() => navigate(-1)} variant="secondary">
            Voltar
          </Button>
          {canCreateMeta && (
            <Button
              onClick={() => navigate(`/metas/nova?colaborador_id=${parsedId}`)}
              variant="primary"
            >
              Criar Nova Meta
            </Button>
          )}
        </div>
      </div>

      <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-6 shadow-md">
        <MetasColaboradorView colaboradorId={parsedId} />
      </div>
    </div>
  );
}
