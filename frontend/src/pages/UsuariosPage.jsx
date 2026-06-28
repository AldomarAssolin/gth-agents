import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Table from "../components/ui/Table";
import Button from "../components/ui/Button";
import Loading from "../components/ui/Loading";
import EmptyState from "../components/ui/EmptyState";
import ErrorMessage from "../components/ui/ErrorMessage";
import UsuarioForm from "../features/configuracoes/UsuarioForm";
import PerfilUsuarioBadge from "../features/configuracoes/PerfilUsuarioBadge";
import StatusAtivoBadge from "../features/configuracoes/StatusAtivoBadge";
import {
  listarUsuarios,
  criarUsuario,
  atualizarUsuario,
  ativarUsuario,
  desativarUsuario,
} from "../features/configuracoes/usuariosService";
import { useAuth } from "../features/auth/useAuth";
import { getConfiguracoesErrorMessage } from "../features/configuracoes/configuracoesErrors";

export default function UsuariosPage() {
  const { user } = useAuth();
  const canAccess = ["ADMIN", "RH"].includes(user?.perfil);

  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingUsuario, setEditingUsuario] = useState(null);
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!canAccess) return;

    const controller = new AbortController();

    const fetchUsuarios = async () => {
      try {
        const data = await listarUsuarios({ signal: controller.signal });
        setUsuarios(data);
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

    fetchUsuarios();

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
    if (editingUsuario) {
      const updated = await atualizarUsuario(editingUsuario.id, payload);
      setUsuarios((prev) =>
        prev.map((u) => (u.id === editingUsuario.id ? updated : u))
      );
      setEditingUsuario(null);
    } else {
      const created = await criarUsuario(payload);
      setUsuarios((prev) => [created, ...prev]);
    }
    setShowForm(false);
  };

  const handleToggleStatus = async (usuario) => {
    try {
      const updated = usuario.ativo
        ? await desativarUsuario(usuario.id)
        : await ativarUsuario(usuario.id);
      setUsuarios((prev) =>
        prev.map((u) => (u.id === usuario.id ? updated : u))
      );
    } catch (err) {
      alert(getConfiguracoesErrorMessage(err));
    }
  };

  const handleEditClick = (usuario) => {
    setEditingUsuario(usuario);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleCancelForm = () => {
    setEditingUsuario(null);
    setShowForm(false);
  };

  if (!canAccess) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Configurações - Usuários"
          description="Gerencie os usuários e permissões de acesso"
        />
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage
            title="Acesso Negado"
            message="Você não possui permissão para acessar a configuração de usuários."
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
        title="Usuários"
        description="Gerencie os perfis de acesso, credenciais e permissões no GTH Agents"
        actions={
          <div className="flex items-center space-x-3">
            <Link to="/configuracoes">
              <Button variant="secondary">Voltar</Button>
            </Link>
            {!showForm && (
              <Button onClick={() => setShowForm(true)} variant="primary">
                Novo Usuário
              </Button>
            )}
          </div>
        }
      />

      {showForm && (
        <Card className="max-w-2xl border border-slate-700">
          <h3 className="text-xl font-bold text-white mb-4">
            {editingUsuario ? `Editar Usuário: ${editingUsuario.nome}` : "Cadastrar Novo Usuário"}
          </h3>
          <UsuarioForm
            key={editingUsuario?.id ? `usuario-${editingUsuario.id}` : "usuario-new"}
            onSubmit={handleCreateOrUpdate}
            onCancel={handleCancelForm}
            initialData={editingUsuario}
          />
        </Card>
      )}

      {loading ? (
        <Loading message="Carregando usuários..." />
      ) : loadError ? (
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage title="Erro ao carregar usuários" message={loadError} />
          <Button onClick={handleRetry} variant="primary">
            Tentar Novamente
          </Button>
        </div>
      ) : usuarios.length === 0 ? (
        <EmptyState
          title="Nenhum usuário encontrado"
          description="Cadastre o primeiro usuário administrativo ou operacional."
          actionLabel="Adicionar Usuário"
          onAction={() => setShowForm(true)}
        />
      ) : (
        <Card className="border border-slate-700">
          <Table headers={["ID", "Nome", "E-mail", "Perfil", "Status", "Ações"]} className="[&_table]:min-w-[800px]">
            {usuarios.map((usr) => (
              <tr key={usr.id} className="hover:bg-slate-750 transition-colors">
                <td className="px-6 py-4 text-sm font-semibold text-slate-400">
                  #{usr.id}
                </td>
                <td className="px-6 py-4 font-bold text-white">{usr.nome}</td>
                <td className="px-6 py-4 text-slate-300">{usr.email}</td>
                <td className="px-6 py-4">
                  <PerfilUsuarioBadge perfil={usr.perfil} />
                </td>
                <td className="px-6 py-4">
                  <StatusAtivoBadge ativo={usr.ativo} />
                </td>
                <td className="px-6 py-4 space-x-3">
                  <Button
                    onClick={() => handleEditClick(usr)}
                    variant="secondary"
                    size="sm"
                  >
                    Editar
                  </Button>
                  <Button
                    onClick={() => handleToggleStatus(usr)}
                    variant={usr.ativo ? "danger" : "primary"}
                    size="sm"
                  >
                    {usr.ativo ? "Desativar" : "Ativar"}
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
