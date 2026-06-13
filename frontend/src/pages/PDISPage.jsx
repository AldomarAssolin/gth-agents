import { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { listarPDIs } from "../features/pdis/pdisService";
import { getPDIErrorMessage } from "../features/pdis/pdisErrors";
import PDITable from "../features/pdis/PDITable";
import PDIsColaboradorView from "../features/pdis/PDIsColaboradorView";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import EmptyState from "../components/ui/EmptyState";
import Button from "../components/ui/Button";

export default function PDISPage() {
  const { user } = useAuth();
  const isGestor = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [pdis, setPdis] = useState([]);
  const [colaboradores, setColaboradores] = useState([]);
  const [loading, setLoading] = useState(isGestor);
  const [error, setError] = useState("");

  // Local filters
  const [colaboradorBusca, setColaboradorBusca] = useState("");
  const [statusFiltro, setStatusFiltro] = useState("TODOS");
  const [origemFiltro, setOrigemFiltro] = useState("TODOS");
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!isGestor) return;

    const controller = new AbortController();

    const carregarDados = async () => {
      try {
        setLoading(true);
        setError("");

        const [listPDIs, listColabs] = await Promise.all([
          listarPDIs({ signal: controller.signal }),
          listarColaboradores({ signal: controller.signal }).catch(() => []) // Fallback in case of list collaborators failure
        ]);

        setPdis(listPDIs);
        setColaboradores(listColabs);
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

    carregarDados();

    return () => {
      controller.abort();
    };
  }, [isGestor, retryTrigger]);

  // Map of ID -> Colaborador Name
  const colaboradoresMap = useMemo(() => {
    const map = new Map();
    colaboradores.forEach((c) => {
      map.set(c.id, c.nome);
    });
    return map;
  }, [colaboradores]);

  // Client-side filtering
  const pdisFiltrados = useMemo(() => {
    return pdis.filter((pdi) => {
      const colNome = (colaboradoresMap.get(pdi.colaborador_id) || "").toLowerCase();
      const matchColab = !colaboradorBusca || colNome.includes(colaboradorBusca.toLowerCase()) || String(pdi.colaborador_id).includes(colaboradorBusca);
      const matchStatus = statusFiltro === "TODOS" || pdi.status === statusFiltro;
      const matchOrigem = origemFiltro === "TODOS" || pdi.origem === origemFiltro;
      return matchColab && matchStatus && matchOrigem;
    });
  }, [pdis, colaboradorBusca, statusFiltro, origemFiltro, colaboradoresMap]);

  const handleRetry = () => {
    setRetryTrigger((prev) => prev + 1);
  };

  // 1. Collaborator View (renders own PDIs directly)
  if (!isGestor) {
    if (!user?.colaborador_id) {
      return (
        <div className="space-y-6">
          <PageHeader
            title="PDI (Plano de Desenvolvimento Individual)"
            description="Ações de treinamento, mentoria e desenvolvimento focados no seu crescimento profissional."
          />
          <ErrorMessage
            title="Vínculo de Colaborador Ausente"
            message="Não encontramos um perfil de colaborador associado ao seu usuário. Por favor, contate o RH ou seu gestor."
          />
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <PageHeader
          title="PDI (Plano de Desenvolvimento Individual)"
          description="Ações de treinamento, mentoria e desenvolvimento focados no seu crescimento profissional."
        />
        <Card>
          <PDIsColaboradorView colaboradorId={user.colaborador_id} />
        </Card>
      </div>
    );
  }

  // 2. Manager View
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <PageHeader
          title="PDI (Plano de Desenvolvimento Individual)"
          description="Monitore e gerencie as ações de desenvolvimento dos colaboradores."
        />
        <div className="shrink-0">
          <Link to="/pdis/novo">
            <Button variant="primary">Criar Novo PDI</Button>
          </Link>
        </div>
      </div>

      {loading ? (
        <Loading message="Carregando planos de desenvolvimento..." />
      ) : error ? (
        <div className="space-y-4">
          <ErrorMessage title="Erro ao carregar dados" message={error} />
          <div>
            <Button onClick={handleRetry} variant="primary">
              Tentar novamente
            </Button>
          </div>
        </div>
      ) : (
        <Card>
          {/* Local Filters Section */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="flex flex-col space-y-1.5">
              <label htmlFor="colab_busca" className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Buscar Colaborador
              </label>
              <input
                id="colab_busca"
                type="text"
                value={colaboradorBusca}
                onChange={(e) => setColaboradorBusca(e.target.value)}
                placeholder="Nome ou ID do colaborador..."
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="flex flex-col space-y-1.5">
              <label htmlFor="status_filtro" className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Filtrar por Status
              </label>
              <select
                id="status_filtro"
                value={statusFiltro}
                onChange={(e) => setStatusFiltro(e.target.value)}
                className="bg-slate-700 border border-slate-600 rounded-lg text-slate-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="TODOS">Todos os Status</option>
                <option value="RASCUNHO">Rascunho</option>
                <option value="ATIVO">Ativo</option>
                <option value="CONCLUIDO">Concluído</option>
                <option value="CANCELADO">Cancelado</option>
              </select>
            </div>

            <div className="flex flex-col space-y-1.5">
              <label htmlFor="origem_filtro" className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Filtrar por Origem
              </label>
              <select
                id="origem_filtro"
                value={origemFiltro}
                onChange={(e) => setOrigemFiltro(e.target.value)}
                className="bg-slate-700 border border-slate-600 rounded-lg text-slate-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="TODOS">Todas as Origens</option>
                <option value="MANUAL">Manual</option>
                <option value="AVALIACAO">Avaliação</option>
                <option value="FEEDBACK">Feedback</option>
                <option value="META">Meta</option>
                <option value="INDICACAO_LIDER">Indicação do Líder</option>
                <option value="AGENTE_IA">Agente IA</option>
              </select>
            </div>
          </div>

          {pdisFiltrados.length === 0 ? (
            <EmptyState
              title={pdis.length === 0 ? "Sem planos cadastrados" : "Nenhum PDI encontrado"}
              message={
                pdis.length === 0
                  ? "Atualmente não há Planos de Desenvolvimento Individual registrados."
                  : "Nenhum plano corresponde aos filtros aplicados. Tente ajustar a busca."
              }
            />
          ) : (
            <PDITable pdis={pdisFiltrados} colaboradoresMap={colaboradoresMap} showColaborador={true} />
          )}
        </Card>
      )}
    </div>
  );
}
