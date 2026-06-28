import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Table from "../components/ui/Table";
import Button from "../components/ui/Button";
import Loading from "../components/ui/Loading";
import EmptyState from "../components/ui/EmptyState";
import ErrorMessage from "../components/ui/ErrorMessage";
import FuncaoForm from "../features/configuracoes/FuncaoForm";
import StatusAtivoBadge from "../features/configuracoes/StatusAtivoBadge";
import {
  listarFuncoes,
  criarFuncao,
  atualizarFuncao,
  ativarFuncao,
  desativarFuncao,
} from "../features/configuracoes/funcoesService";
import { useAuth } from "../features/auth/useAuth";
import { getConfiguracoesErrorMessage } from "../features/configuracoes/configuracoesErrors";

export default function FuncoesPage() {
  const { user } = useAuth();
  const canAccess = ["ADMIN", "RH"].includes(user?.perfil);

  const [funcoes, setFuncoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingFuncao, setEditingFuncao] = useState(null);
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!canAccess) return;

    const controller = new AbortController();

    const fetchFuncoes = async () => {
      try {
        const data = await listarFuncoes({ signal: controller.signal });
        setFuncoes(data);
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

    fetchFuncoes();

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
    if (editingFuncao) {
      const updated = await atualizarFuncao(editingFuncao.id, payload);
      setFuncoes((prev) =>
        prev.map((f) => (f.id === editingFuncao.id ? updated : f))
      );
      setEditingFuncao(null);
    } else {
      const created = await criarFuncao(payload);
      setFuncoes((prev) => [created, ...prev]);
    }
    setShowForm(false);
  };

  const handleToggleStatus = async (funcao) => {
    try {
      const updated = funcao.ativo
        ? await desativarFuncao(funcao.id)
        : await ativarFuncao(funcao.id);
      setFuncoes((prev) =>
        prev.map((f) => (f.id === funcao.id ? updated : f))
      );
    } catch (err) {
      alert(getConfiguracoesErrorMessage(err));
    }
  };

  const handleEditClick = (funcao) => {
    setEditingFuncao(funcao);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCancelForm = () => {
    setEditingFuncao(null);
    setShowForm(false);
  };

  if (!canAccess) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Configurações - Funções"
          description="Gerencie os cargos e funções do sistema"
        />
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage
            title="Acesso Negado"
            message="Você não possui permissão para acessar a configuração de funções."
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
        title="Funções"
        description="Gerencie os cargos e atribuições da equipe no GTH Agents"
        actions={
          <div className="flex items-center space-x-3">
            <Link to="/configuracoes">
              <Button variant="secondary">Voltar</Button>
            </Link>
            {!showForm && (
              <Button onClick={() => setShowForm(true)} variant="primary">
                Nova Função
              </Button>
            )}
          </div>
        }
      />

      {showForm && (
        <Card className="max-w-2xl border border-slate-700">
          <h3 className="text-xl font-bold text-white mb-4">
            {editingFuncao ? `Editar Função: ${editingFuncao.nome}` : "Cadastrar Nova Função"}
          </h3>
          <FuncaoForm
            key={editingFuncao?.id ? `funcao-${editingFuncao.id}` : "funcao-new"}
            onSubmit={handleCreateOrUpdate}
            onCancel={handleCancelForm}
            initialData={editingFuncao}
          />
        </Card>
      )}

      {loading ? (
        <Loading message="Carregando funções..." />
      ) : loadError ? (
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage title="Erro ao carregar funções" message={loadError} />
          <Button onClick={handleRetry} variant="primary">
            Tentar Novamente
          </Button>
        </div>
      ) : funcoes.length === 0 ? (
        <EmptyState
          title="Nenhuma função encontrada"
          description="Cadastre a primeira função para organizar os cargos dos colaboradores."
          actionLabel="Adicionar Função"
          onAction={() => setShowForm(true)}
        />
      ) : (
        <Card className="border border-slate-700">
          <Table headers={["ID", "Nome da Função", "Descrição", "Status", "Ações"]} className="[&_table]:min-w-[700px]">
            {funcoes.map((funcao) => (
              <tr key={funcao.id} className="hover:bg-slate-750 transition-colors">
                <td className="px-6 py-4 text-sm font-semibold text-slate-400">
                  #{funcao.id}
                </td>
                <td className="px-6 py-4 font-bold text-white">{funcao.nome}</td>
                <td className="px-6 py-4 text-slate-300 max-w-xs truncate">
                  {funcao.descricao || <span className="text-slate-500 italic">Sem descrição</span>}
                </td>
                <td className="px-6 py-4">
                  <StatusAtivoBadge ativo={funcao.ativo} />
                </td>
                <td className="px-6 py-4 space-x-3">
                  <Button
                    onClick={() => handleEditClick(funcao)}
                    variant="secondary"
                    size="sm"
                  >
                    Editar
                  </Button>
                  <Button
                    onClick={() => handleToggleStatus(funcao)}
                    variant={funcao.ativo ? "danger" : "primary"}
                    size="sm"
                  >
                    {funcao.ativo ? "Desativar" : "Ativar"}
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
