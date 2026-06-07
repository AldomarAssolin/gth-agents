import { useState, useEffect } from "react";
import { listarMetasPorColaborador } from "./metasService";
import { getMetaErrorMessage } from "./metasErrors";
import MetasTable from "./MetasTable";
import Loading from "../../components/ui/Loading";
import ErrorMessage from "../../components/ui/ErrorMessage";
import EmptyState from "../../components/ui/EmptyState";
import Button from "../../components/ui/Button";

export default function MetasColaboradorView({ colaboradorId }) {
  const parsedId = Number(colaboradorId);
  const isIdValido = Number.isInteger(parsedId) && parsedId > 0;

  const [metas, setMetas] = useState([]);
  const [loading, setLoading] = useState(isIdValido);
  const [error, setError] = useState(isIdValido ? "" : "Identificador de colaborador inválido.");
  const [statusFiltro, setStatusFiltro] = useState("TODOS");
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!isIdValido) return;

    const controller = new AbortController();

    const carregarMetas = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await listarMetasPorColaborador(parsedId, {
          signal: controller.signal,
        });
        setMetas(data);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setError(getMetaErrorMessage(err));
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarMetas();

    return () => {
      controller.abort();
    };
  }, [parsedId, isIdValido, retryTrigger]);

  const handleRetry = () => {
    setRetryTrigger((prev) => prev + 1);
  };

  if (!isIdValido) {
    return <ErrorMessage title="Erro de Validação" message={error} />;
  }

  if (loading) {
    return <Loading message="Carregando metas do colaborador..." />;
  }

  if (error) {
    return (
      <div className="space-y-4">
        <ErrorMessage title="Erro ao carregar metas" message={error} />
        <div>
          <Button onClick={handleRetry} variant="primary">
            Tentar novamente
          </Button>
        </div>
      </div>
    );
  }

  // Filtragem local das metas por status
  const metasFiltradas =
    statusFiltro === "TODOS"
      ? metas
      : metas.filter((meta) => meta.status === statusFiltro);

  const statusOptions = [
    { label: "Todos os Status", value: "TODOS" },
    { label: "Pendente", value: "PENDENTE" },
    { label: "Em andamento", value: "EM_ANDAMENTO" },
    { label: "Concluída", value: "CONCLUIDA" },
    { label: "Atrasada", value: "ATRASADA" },
    { label: "Cancelada", value: "CANCELADA" },
  ];

  return (
    <div className="space-y-4">
      {metas.length > 0 && (
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between bg-slate-800/40 p-4 rounded-lg border border-slate-700/60 gap-3">
          <div className="flex flex-col sm:flex-row sm:items-center gap-3">
            <span className="text-sm font-medium text-slate-300 shrink-0">Filtrar por Status:</span>
            <div className="flex flex-wrap gap-2">
              {statusOptions.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setStatusFiltro(opt.value)}
                  className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
                    statusFiltro === opt.value
                      ? "bg-indigo-600 text-white shadow-sm"
                      : "bg-slate-700 text-slate-300 hover:bg-slate-600 hover:text-white"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {metasFiltradas.length === 0 ? (
        <EmptyState
          title={metas.length === 0 ? "Nenhuma meta cadastrada" : "Nenhuma meta corresponde ao filtro"}
          message={
            metas.length === 0
              ? "Este colaborador ainda não possui metas atribuídas para o período."
              : "Tente selecionar outra opção de filtro de status."
          }
        />
      ) : (
        <MetasTable metas={metasFiltradas} />
      )}
    </div>
  );
}
