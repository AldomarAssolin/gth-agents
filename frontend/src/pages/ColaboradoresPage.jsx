import { Link, useNavigate } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Table from "../components/ui/Table";
import Badge from "../components/ui/Badge";
import Button from "../components/ui/Button";

const mockColaboradores = [
  { id: 1, nome: "João Silva", cargo: "Desenvolvedor Backend", status: "Ativo" },
  { id: 2, nome: "Maria Santos", cargo: "Desenvolvedora Frontend", status: "Ativo" },
  { id: 3, nome: "Pedro Souza", cargo: "Product Owner", status: "Inativo" },
];

export default function ColaboradoresPage() {
  const navigate = useNavigate();

  const handleCreateNew = () => {
    navigate("/colaboradores/novo");
  };

  const headerActions = (
    <Button onClick={handleCreateNew} variant="primary">
      Novo Colaborador
    </Button>
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Colaboradores"
        description="Gerencie os membros da sua equipe e acesse seus históricos"
        actions={headerActions}
      />

      <Table headers={["ID", "Nome", "Cargo", "Status", "Ações"]}>
        {mockColaboradores.map((colaborador) => (
          <tr key={colaborador.id} className="hover:bg-slate-700/30 transition-colors">
            <td className="px-6 py-4 text-sm">{colaborador.id}</td>
            <td className="px-6 py-4 text-sm font-semibold text-white">{colaborador.nome}</td>
            <td className="px-6 py-4 text-sm text-slate-300">{colaborador.cargo}</td>
            <td className="px-6 py-4 text-sm">
              <Badge variant={colaborador.status === "Ativo" ? "success" : "secondary"}>
                {colaborador.status}
              </Badge>
            </td>
            <td className="px-6 py-4 text-sm space-x-3">
              <Link
                to={`/colaboradores/${colaborador.id}`}
                className="text-indigo-400 hover:text-indigo-300 transition-colors font-semibold"
              >
                Ver Detalhes
              </Link>
              <Link
                to={`/colaboradores/${colaborador.id}/evolucao`}
                className="text-emerald-400 hover:text-emerald-300 transition-colors font-semibold"
              >
                Ver Evolução
              </Link>
            </td>
          </tr>
        ))}
      </Table>
    </div>
  );
}
