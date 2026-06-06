import { useNavigate } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import Select from "../components/ui/Select";
import Button from "../components/ui/Button";

export default function NovoColaboradorPage() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/colaboradores");
  };

  const handleCancel = () => {
    navigate("/colaboradores");
  };

  const cargoOptions = [
    { value: "", label: "Selecione um cargo..." },
    { value: "backend", label: "Desenvolvedor Backend" },
    { value: "frontend", label: "Desenvolvedora Frontend" },
    { value: "po", label: "Product Owner" },
    { value: "qa", label: "Analista de QA" }
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Cadastrar Colaborador"
        description="Adicione um novo colaborador à equipe do GTH Agents"
      />

      <Card className="max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Nome Completo"
            required
            placeholder="Nome do colaborador"
          />
          <Input
            label="E-mail Corporativo"
            type="email"
            required
            placeholder="exemplo@empresa.com"
          />
          <Select
            label="Cargo"
            required
            options={cargoOptions}
          />
          
          <div className="flex justify-end space-x-3 pt-4 border-t border-slate-700">
            <Button
              type="button"
              variant="secondary"
              onClick={handleCancel}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="primary"
            >
              Salvar Cadastro
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
