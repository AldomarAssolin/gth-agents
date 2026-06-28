import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Table from "../components/ui/Table";
import Button from "../components/ui/Button";
import Loading from "../components/ui/Loading";
import EmptyState from "../components/ui/EmptyState";
import ErrorMessage from "../components/ui/ErrorMessage";
import SetorForm from "../features/configuracoes/SetorForm";
import StatusAtivoBadge from "../features/configuracoes/StatusAtivoBadge";
import {
  listarSetores,
  criarSetor,
  atualizarSetor,
  ativarSetor,
  desativarSetor,
} from "../features/configuracoes/setoresService";
import { useAuth } from "../features/auth/useAuth";
import { getConfiguracoesErrorMessage } from "../features/configuracoes/configuracoesErrors";

export default function SetoresPage() {
  const { user } = useAuth();
  const canAccess = ["ADMIN", "RH"].includes(user?.perfil);

  const [setores, setSetores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingSetor, setEditingSetor] = useState(null);
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!canAccess) return;

    const controller = new AbortController();

    const fetchSetores = async () => {
      try {
        const data = await listarSetores({ signal: controller.signal });
        setSetores(data);
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

    fetchSetores();

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
    if (editingSetor) {
      const updated = await atualizarSetor(editingSetor.id, payload);
      setSetores((prev) =>
        prev.map((s) => (s.id === editingSetor.id ? updated : s))
      );
      setEditingSetor(null);
    } else {
      const created = await criarSetor(payload);
      setSetores((prev) => [created, ...prev]);
    }
    setShowForm(false);
  };

  const handleToggleStatus = async (setor) => {
    try {
      const updated = setor.ativo
        ? await desativarSetor(setor.id)
        : await ativarSetor(setor.id);
      setSetores((prev) =>
        prev.map((s) => (s.id === setor.id ? updated : s))
      );
    } catch (err) {
      alert(getConfiguracoesErrorMessage(err));
    }
  };

  const handleEditClick = (setor) => {
    setEditingSetor(setor);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCancelForm = () => {
    setEditingSetor(null);
    setShowForm(false);
  };

  if (!canAccess) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Configurações - Setores"
          description="Gerencie os setores organizacionais do sistema"
        />
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage
            title="Acesso Negado"
            message="Você não possui permissão para acessar a configuração de setores."
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
        title="Setores"
        description="Gerencie a estrutura de setores e áreas do GTH Agents"
        actions={
          <div className="flex items-center space-x-3">
            <Link to="/configuracoes">
              <Button variant="secondary">Voltar</Button>
            </Link>
            {!showForm && (
              <Button onClick={() => setShowForm(true)} variant="primary">
                Novo Setor
              </Button>
            )}
          </div>
        }
      />

      {showForm && (
        <Card className="max-w-2xl border border-slate-700">
          <h3 className="text-xl font-bold text-white mb-4">
            {editingSetor ? `Editar Setor: ${editingSetor.nome}` : "Cadastrar Novo Setor"}
          </h3>
          <SetorForm
            key={editingSetor?.id ? `setor-${editingSetor.id}` : "setor-new"}
            onSubmit={handleCreateOrUpdate}
            onCancel={handleCancelForm}
            initialData={editingSetor}
          />
        </Card>
      )}

      {loading ? (
        <Loading message="Carregando setores..." />
      ) : loadError ? (
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage title="Erro ao carregar setores" message={loadError} />
          <Button onClick={handleRetry} variant="primary">
            Tentar Novamente
          </Button>
        </div>
      ) : setores.length === 0 ? (
        <EmptyState
          title="Nenhum setor encontrado"
          description="Cadastre o primeiro setor para organizar seus colaboradores."
          actionLabel="Adicionar Setor"
          onAction={() => setShowForm(true)}
        />
      ) : (
        <Card className="border border-slate-700">
          <Table headers={["ID", "Nome do Setor", "Descrição", "Status", "Ações"]} className="[&_table]:min-w-[700px]">
            {setores.map((setor) => (
              <tr key={setor.id} className="hover:bg-slate-750 transition-colors">
                <td className="px-6 py-4 text-sm font-semibold text-slate-400">
                  #{setor.id}
                </td>
                <td className="px-6 py-4 font-bold text-white">{setor.nome}</td>
                <td className="px-6 py-4 text-slate-300 max-w-xs truncate">
                  {setor.descricao || <span className="text-slate-500 italic">Sem descrição</span>}
                </td>
                <td className="px-6 py-4">
                  <StatusAtivoBadge ativo={setor.ativo} />
                </td>
                <td className="px-6 py-4 space-x-3">
                  <Button
                    onClick={() => handleEditClick(setor)}
                    variant="secondary"
                    size="sm"
                  >
                    Editar
                  </Button>
                  <Button
                    onClick={() => handleToggleStatus(setor)}
                    variant={setor.ativo ? "danger" : "primary"}
                    size="sm"
                  >
                    {setor.ativo ? "Desativar" : "Ativar"}
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
