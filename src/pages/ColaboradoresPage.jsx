import { Link } from "react-router-dom";
import Layout from "../layouts/Layout";

const mockColaboradores = [
  { id: 1, nome: "João Silva", cargo: "Desenvolvedor Backend", status: "Ativo" },
  { id: 2, nome: "Maria Santos", cargo: "Desenvolvedora Frontend", status: "Ativo" },
  { id: 3, nome: "Pedro Souza", cargo: "Product Owner", status: "Inativo" },
];

export default function ColaboradoresPage() {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">Colaboradores</h1>
            <p className="text-slate-400 mt-1">Gerenciamento de membros da equipe</p>
          </div>
        </div>

        <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-md overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-700/50 border-b border-slate-700 text-slate-300 text-sm font-semibold">
                <th className="px-6 py-4">ID</th>
                <th className="px-6 py-4">Nome</th>
                <th className="px-6 py-4">Cargo</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700 text-slate-200">
              {mockColaboradores.map((colaborador) => (
                <tr key={colaborador.id} className="hover:bg-slate-700/30 transition-colors">
                  <td className="px-6 py-4">{colaborador.id}</td>
                  <td className="px-6 py-4 font-medium text-white">{colaborador.nome}</td>
                  <td className="px-6 py-4 text-slate-300">{colaborador.cargo}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        colaborador.status === "Ativo"
                          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/25"
                          : "bg-slate-500/10 text-slate-400 border border-slate-500/25"
                      }`}
                    >
                      {colaborador.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right space-x-3">
                    <Link
                      to={`/colaboradores/${colaborador.id}`}
                      className="text-indigo-400 hover:text-indigo-300 transition-colors font-medium text-sm"
                    >
                      Ver Detalhes
                    </Link>
                    <Link
                      to={`/colaboradores/${colaborador.id}/evolucao`}
                      className="text-emerald-400 hover:text-emerald-300 transition-colors font-medium text-sm"
                    >
                      Ver Evolução
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Layout>
  );
}
