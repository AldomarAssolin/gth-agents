import { useParams, Link } from "react-router-dom";
import Layout from "../layouts/Layout";

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

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Link
            to="/colaboradores"
            className="text-slate-400 hover:text-white transition-colors"
          >
            &larr; Voltar para a lista
          </Link>
        </div>

        <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-md p-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-700 pb-6 mb-6">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-white">{colaborador.nome}</h1>
              <p className="text-indigo-400 mt-1">{colaborador.cargo}</p>
            </div>
            <span
              className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold mt-4 md:mt-0 ${
                colaborador.status === "Ativo"
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/25"
                  : "bg-slate-500/10 text-slate-400 border border-slate-500/25"
              }`}
            >
              {colaborador.status}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-slate-400">E-mail Corporativo</h3>
              <p className="text-white text-lg mt-1 font-medium">{colaborador.email}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-slate-400">Data de Admissão</h3>
              <p className="text-white text-lg mt-1 font-medium">{colaborador.dataAdmissao}</p>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-700 flex space-x-4">
            <Link
              to={`/colaboradores/${id}/evolucao`}
              className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg shadow-md transition-all text-sm inline-flex items-center"
            >
              Visualizar Histórico de Evolução
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}
