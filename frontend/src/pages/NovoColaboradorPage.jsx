import { useNavigate } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";
import ColaboradorForm from "../features/colaboradores/ColaboradorForm";
import { useAuth } from "../features/auth/useAuth";
import { criarColaborador } from "../features/colaboradores/colaboradoresService";

export default function NovoColaboradorPage() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const canCreateColaborador = ["ADMIN", "RH"].includes(user?.perfil);

  const handleSubmit = async (payload) => {
    const result = await criarColaborador(payload);
    if (result && result.id) {
      navigate(`/colaboradores/${result.id}`);
    } else {
      navigate("/colaboradores");
    }
  };

  const handleCancel = () => {
    navigate("/colaboradores");
  };

  if (!canCreateColaborador) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Cadastrar Colaborador"
          description="Adicione um novo colaborador à equipe"
        />
        <div className="space-y-4">
          <ErrorMessage
            title="Acesso Negado"
            message="Você não possui permissão para cadastrar colaboradores."
          />
          <div>
            <Button onClick={handleCancel} variant="secondary">
              Voltar para a Lista
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Cadastrar Colaborador"
        description="Adicione um novo colaborador à equipe do GTH Agents"
      />

      <Card className="max-w-2xl">
        <ColaboradorForm onSubmit={handleSubmit} onCancel={handleCancel} />
      </Card>
    </div>
  );
}
