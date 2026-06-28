import { Link } from "react-router-dom";
import Table from "../../components/ui/Table";
import StatusPDIBadge from "./StatusPDIBadge";
import { formatarData, traduzirOrigemPDI } from "./pdisFormatters";
import Button from "../../components/ui/Button";

export default function PDITable({ pdis = [], colaboradoresMap = new Map(), showColaborador = true }) {
  const headers = showColaborador
    ? ["Colaborador", "PDI", "Origem", "Início", "Fim", "Status", "Ações (Concluídas/Total)", "Ações"]
    : ["PDI", "Origem", "Início", "Fim", "Status", "Ações (Concluídas/Total)", "Ações"];

  return (
    <Table headers={headers} className="[&_table]:min-w-[800px]">
      {pdis.map((pdi) => {
        const totalAcoes = Array.isArray(pdi.acoes) ? pdi.acoes.length : 0;
        const acoesConcluidas = Array.isArray(pdi.acoes)
          ? pdi.acoes.filter((a) => a.status === "CONCLUIDA").length
          : 0;
        
        const colaboradorNome = colaboradoresMap.get(pdi.colaborador_id) || `Colaborador #${pdi.colaborador_id}`;

        return (
          <tr key={pdi.id} className="hover:bg-slate-700/30 transition-colors">
            {showColaborador && (
              <td className="px-6 py-4 text-white font-medium whitespace-nowrap">
                {colaboradorNome}
              </td>
            )}
            <td className="px-6 py-4">
              <div className="text-white font-semibold">{pdi.titulo}</div>
              <div className="text-slate-400 text-xs mt-0.5 max-w-md line-clamp-2">{pdi.descricao}</div>
            </td>
            <td className="px-6 py-4 text-slate-300 text-sm whitespace-nowrap">
              {traduzirOrigemPDI(pdi.origem)}
            </td>
            <td className="px-6 py-4 text-slate-300 text-sm whitespace-nowrap">
              {formatarData(pdi.data_inicio)}
            </td>
            <td className="px-6 py-4 text-slate-300 text-sm whitespace-nowrap">
              {formatarData(pdi.data_fim)}
            </td>
            <td className="px-6 py-4 whitespace-nowrap">
              <StatusPDIBadge status={pdi.status} />
            </td>
            <td className="px-6 py-4 text-slate-300 text-sm whitespace-nowrap text-center">
              <span className="font-semibold text-indigo-400">{acoesConcluidas}</span>
              <span className="text-slate-500"> / </span>
              <span className="text-slate-400">{totalAcoes}</span>
            </td>
            <td className="px-6 py-4 whitespace-nowrap">
              <Link to={`/pdis/${pdi.id}`}>
                <Button variant="outline" size="sm">
                  Ver Detalhes
                </Button>
              </Link>
            </td>
          </tr>
        );
      })}
    </Table>
  );
}
