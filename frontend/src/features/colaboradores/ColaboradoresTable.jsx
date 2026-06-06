import { Link } from "react-router-dom";
import Table from "../../components/ui/Table";
import StatusColaboradorBadge from "./StatusColaboradorBadge";
import { resolverNomeSetor, resolverNomeFuncao } from "./colaboradoresHelpers";

export default function ColaboradoresTable({ colaboradores = [], setores = [], funcoes = [] }) {
  const headers = [
    "ID",
    "Nome",
    "Matrícula",
    "E-mail",
    "Setor",
    "Função",
    "Status",
    "Ações",
  ];

  return (
    <Table headers={headers} className="[&_table]:min-w-[900px]">
      {colaboradores.map((colaborador) => (
        <tr key={colaborador.id} className="hover:bg-slate-700/30 transition-colors">
          <td className="px-6 py-4 text-sm">{colaborador.id}</td>
          <td className="px-6 py-4 text-sm font-semibold text-white">
            {colaborador.nome}
          </td>
          <td className="px-6 py-4 text-sm text-slate-300">
            {colaborador.matricula}
          </td>
          <td className="px-6 py-4 text-sm text-slate-300">
            {colaborador.email || "Não informado"}
          </td>
          <td className="px-6 py-4 text-sm text-slate-300">
            {resolverNomeSetor(colaborador, setores)}
          </td>
          <td className="px-6 py-4 text-sm text-slate-300">
            {resolverNomeFuncao(colaborador, funcoes)}
          </td>
          <td className="px-6 py-4 text-sm">
            <StatusColaboradorBadge status={colaborador.status} />
          </td>
          <td className="px-6 py-4 text-sm space-x-3">
            <Link
              to={`/colaboradores/${colaborador.id}`}
              className="text-indigo-400 hover:text-indigo-300 transition-colors font-semibold"
              aria-label={`Ver detalhes de ${colaborador.nome}`}
            >
              Ver Detalhes
            </Link>
            <Link
              to={`/colaboradores/${colaborador.id}/evolucao`}
              className="text-emerald-400 hover:text-emerald-300 transition-colors font-semibold"
              aria-label={`Ver evolução de ${colaborador.nome}`}
            >
              Ver Evolução
            </Link>
          </td>
        </tr>
      ))}
    </Table>
  );
}
