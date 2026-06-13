import { useState, useEffect } from "react";
import { listarPDIsPorColaborador } from "./pdisService";
import { getPDIErrorMessage } from "./pdisErrors";
import PDITable from "./PDITable";
import Loading from "../../components/ui/Loading";
import ErrorMessage from "../../components/ui/ErrorMessage";
import EmptyState from "../../components/ui/EmptyState";
import Button from "../../components/ui/Button";

export default function PDIsColaboradorView({ colaboradorId }) {
  const parsedId = Number(colaboradorId);
  const isIdValido = Number.isInteger(parsedId) && parsedId > 0;

  const [pdis, setPdis] = useState([]);
  const [loading, setLoading] = useState(isIdValido);
  const [error, setError] = useState(isIdValido ? "" : "Identificador de colaborador inválido.");
  const [statusFiltro, setStatusFiltro] = useState("TODOS");
  const [origemFiltro, setOrigemFiltro] = useState("TODOS");
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!isIdValido) return;

    const controller = new AbortController();

    const carregarPDIs = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await listarPDIsPorColaborador(parsedId, {
          signal: controller.signal,
        });
        setPdis(data);
      } catch (err) {
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED") {
          setError(getPDIErrorMessage(err));
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarPDIs();

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
    return <Loading message="Carregando PDIs do colaborador..." />;
  }

  if (error) {
    return (
      <div className="space-y-4">
        <ErrorMessage title="Erro ao carregar PDIs" message={error} />
        <div>
          <Button onClick={handleRetry} variant="primary">
            Tentar novamente
          </Button>
        </div>
      </div>
    );
  }

  // Local filtering
  const pdisFiltrados = pdis.filter((pdi) => {
    const matchStatus = statusFiltro === "TODOS" || pdi.status === statusFiltro;
    const matchOrigem = origemFiltro === "TODOS" || pdi.origem === origemFiltro;
    return matchStatus && matchOrigem;
  });

  const statusOptions = [
    { label: "Todos os Status", value: "TODOS" },
    { label: "Rascunho", value: "RASCUNHO" },
    { label: "Ativo", value: "ATIVO" },
    { label: "Concluído", value: "CONCLUIDO" },
    { label: "Cancelado", value: "CANCELADO" },
  ];

  const origemOptions = [
    { label: "Todas as Origens", value: "TODOS" },
    { label: "Manual", value: "MANUAL" },
    { label: "Avaliação", value: "AVALIACAO" },
    { label: "Feedback", value: "FEEDBACK" },
    { label: "Meta", value: "META" },
    { label: "Indicação do Líder", value: "INDICACAO_LIDER" },
    { label: "Agente IA", value: "AGENTE_IA" },
  ];

  return (
    <div className="space-y-4">
      {pdis.length > 0 && (
        <div className="flex flex-col md:flex-row md:items-center justify-between bg-slate-800/40 p-4 rounded-lg border border-slate-700/60 gap-4">
          <div className="flex flex-col sm:flex-row gap-4 w-full">
            <div className="flex flex-col space-y-1.5 flex-1">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Filtrar por Status</label>
              <select
                value={statusFiltro}
                onChange={(e) => setStatusFiltro(e.target.value)}
                className="bg-slate-700 border border-slate-600 rounded-lg text-slate-100 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                {statusOptions.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="flex flex-col space-y-1.5 flex-1">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Filtrar por Origem</label>
              <select
                value={origemFiltro}
                onChange={(e) => setOrigemFiltro(e.target.value)}
                className="bg-slate-700 border border-slate-600 rounded-lg text-slate-100 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                {origemOptions.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {pdisFiltrados.length === 0 ? (
        <EmptyState
          title={pdis.length === 0 ? "Nenhum PDI cadastrado" : "Nenhum PDI corresponde ao filtro"}
          message={
            pdis.length === 0
              ? "Este colaborador ainda não possui Planos de Desenvolvimento Individual."
              : "Tente ajustar as opções dos filtros de status ou origem."
          }
        />
      ) : (
        <PDITable pdis={pdisFiltrados} showColaborador={false} />
      )}
    </div>
  );
}
