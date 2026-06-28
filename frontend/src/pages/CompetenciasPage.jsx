import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Table from "../components/ui/Table";
import Button from "../components/ui/Button";
import Loading from "../components/ui/Loading";
import EmptyState from "../components/ui/EmptyState";
import ErrorMessage from "../components/ui/ErrorMessage";
import CompetenciaForm from "../features/configuracoes/CompetenciaForm";
import TipoCompetenciaBadge from "../features/configuracoes/TipoCompetenciaBadge";
import StatusAtivoBadge from "../features/configuracoes/StatusAtivoBadge";
import {
  listarCompetencias,
  criarCompetencia,
  atualizarCompetencia,
  ativarCompetencia,
  desativarCompetencia,
} from "../features/configuracoes/competenciasService";
import { useAuth } from "../features/auth/useAuth";
import { getConfiguracoesErrorMessage } from "../features/configuracoes/configuracoesErrors";

export default function CompetenciasPage() {
  const { user } = useAuth();
  const canAccess = ["ADMIN", "RH"].includes(user?.perfil);

  const [competencias, setCompetencias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingCompetencia, setEditingCompetencia] = useState(null);
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!canAccess) return;

    const controller = new AbortController();

    const fetchCompetencias = async () => {
      try {
        const data = await listarCompetencias({ signal: controller.signal });
        setCompetencias(data);
        setLoadError("");
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setLoadError(getConfiguracoesErrorMessage(err));
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    fetchCompetencias();

    return () => {
      controller.abort();
    };
  }, [canAccess, retryTrigger]);

  const handleRetry = () => {
    setLoading(true);
    setLoadError("");
    setRetryTrigger((prev) => prev + 1);
  };

  const handleCreateOrUpdate = async (payload) => {
    if (editingCompetencia) {
      const updated = await atualizarCompetencia(editingCompetencia.id, payload);
      setCompetencias((prev) =>
        prev.map((c) => (c.id === editingCompetencia.id ? updated : c))
      );
      setEditingCompetencia(null);
    } else {
      const created = await criarCompetencia(payload);
      setCompetencias((prev) => [created, ...prev]);
    }
    setShowForm(false);
  };

  const handleToggleStatus = async (competencia) => {
    try {
      const updated = competencia.ativo
        ? await desativarCompetencia(competencia.id)
        : await ativarCompetencia(competencia.id);
      setCompetencias((prev) =>
        prev.map((c) => (c.id === competencia.id ? updated : c))
      );
    } catch (err) {
      alert(getConfiguracoesErrorMessage(err));
    }
  };

  const handleEditClick = (competencia) => {
    setEditingCompetencia(competencia);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCancelForm = () => {
    setEditingCompetencia(null);
    setShowForm(false);
  };

  if (!canAccess) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Configurações - Competências"
          description="Gerencie as competências de avaliação do sistema"
        />
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage
            title="Acesso Negado"
            message="Você não possui permissão para acessar a configuração de competências."
          />
          <div>
            <Link to="/">
              <Button variant="secondary">Voltar ao Início</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Competências"
        description="Gerencie as competências técnicas, comportamentais e organizacionais do GTH Agents"
        actions={
          <div className="flex items-center space-x-3">
            <Link to="/configuracoes">
              <Button variant="secondary">Voltar</Button>
            </Link>
            {!showForm && (
              <Button onClick={() => setShowForm(true)} variant="primary">
                Nova Competência
              </Button>
            )}
          </div>
        }
      />

      {showForm && (
        <Card className="max-w-2xl border border-slate-700">
          <h3 className="text-xl font-bold text-white mb-4">
            {editingCompetencia ? `Editar Competência: ${editingCompetencia.nome}` : "Cadastrar Nova Competência"}
          </h3>
          <CompetenciaForm
            key={editingCompetencia?.id ? `competencia-${editingCompetencia.id}` : "competencia-new"}
            onSubmit={handleCreateOrUpdate}
            onCancel={handleCancelForm}
            initialData={editingCompetencia}
          />
        </Card>
      )}

      {loading ? (
        <Loading message="Carregando competências..." />
      ) : loadError ? (
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage title="Erro ao carregar competências" message={loadError} />
          <Button onClick={handleRetry} variant="primary">
            Tentar Novamente
          </Button>
        </div>
      ) : competencias.length === 0 ? (
        <EmptyState
          title="Nenhuma competência encontrada"
          description="Cadastre a primeira competência para avaliar seus colaboradores nas avaliações."
          actionLabel="Adicionar Competência"
          onAction={() => setShowForm(true)}
        />
      ) : (
        <Card className="border border-slate-700">
          <Table headers={["ID", "Nome da Competência", "Tipo", "Descrição", "Peso", "Status", "Ações"]} className="[&_table]:min-w-[850px]">
            {competencias.map((comp) => (
              <tr key={comp.id} className="hover:bg-slate-750 transition-colors">
                <td className="px-6 py-4 text-sm font-semibold text-slate-400">
                  #{comp.id}
                </td>
                <td className="px-6 py-4 font-bold text-white">{comp.nome}</td>
                <td className="px-6 py-4">
                  <TipoCompetenciaBadge tipo={comp.tipo} />
                </td>
                <td className="px-6 py-4 text-slate-300 max-w-xs truncate">
                  {comp.descricao || <span className="text-slate-500 italic">Sem descrição</span>}
                </td>
                <td className="px-6 py-4 text-slate-300 font-semibold">{comp.peso}</td>
                <td className="px-6 py-4">
                  <StatusAtivoBadge ativo={comp.ativo} />
                </td>
                <td className="px-6 py-4 space-x-3">
                  <Button
                    onClick={() => handleEditClick(comp)}
                    variant="secondary"
                    size="sm"
                  >
                    Editar
                  </Button>
                  <Button
                    onClick={() => handleToggleStatus(comp)}
                    variant={comp.ativo ? "danger" : "primary"}
                    size="sm"
                  >
                    {comp.ativo ? "Desativar" : "Ativar"}
                  </Button>
                </td>
              </tr>
            ))}
          </Table>
        </Card>
      )}
    </div>
  );
}
