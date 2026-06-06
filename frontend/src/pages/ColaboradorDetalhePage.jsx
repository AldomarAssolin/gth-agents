import { useParams, Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import Button from "../components/ui/Button";

const mockColaboradoresMap = {
  1: { nome: "João Silva", cargo: "Desenvolvedor Backend", status: "Ativo", email: "joao.silva@empresa.com", dataAdmissao: "2024-01-15" },
  2: { nome: "Maria Santos", cargo: "Desenvolvedora Frontend", status: "Ativo", email: "maria.santos@empresa.com", dataAdmissao: "2024-03-10" },
  3: { nome: "Pedro Souza", cargo: "Product Owner", status: "Inativo", email: "pedro.souza@empresa.com", dataAdmissao: "2023-06-20" },
};

export default function ColaboradorDetalhePage() {
  const { id } = useParams();
  const colaborador = mockColaboradoresMap[id] || {
    nome: "Não encontrado",
    cargo: "Desconhecido",
    status: "Inativo",
    email: "n/a",
    dataAdmissao: "n/a"
  };

  const actions = (
    <Link to={`/colaboradores/${id}/evolucao`}>
      <Button variant="primary">Ver Evolução</Button>
    </Link>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Link
          to="/colaboradores"
          className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
        >
          <span>&larr; Voltar para a lista</span>
        </Link>
      </div>

      <PageHeader
        title={colaborador.nome}
        description={colaborador.cargo}
        actions={colaborador.nome !== "Não encontrado" ? actions : null}
      />

      <Card>
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-700">
          <div>
            <h2 className="text-xl font-bold text-white">Dados do Colaborador</h2>
            <p className="text-slate-400 text-sm mt-1">Informações básicas do cadastro institucional</p>
          </div>
          <div className="mt-4 md:mt-0">
            <Badge variant={colaborador.status === "Ativo" ? "success" : "secondary"}>
              {colaborador.status}
            </Badge>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-sm font-medium text-slate-400">E-mail Corporativo</h3>
            <p className="text-white text-lg mt-1 font-semibold">{colaborador.email}</p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-400">Data de Admissão</h3>
            <p className="text-white text-lg mt-1 font-semibold">{colaborador.dataAdmissao}</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
