import Table from "../../components/ui/Table";
import StatusMetaBadge from "./StatusMetaBadge";
import PrioridadeMetaBadge from "./PrioridadeMetaBadge";
import { formatarData } from "./metasFormatters";

export default function MetasTable({ metas = [] }) {
  const headers = ["Meta", "Prazo", "Prioridade", "Status", "Origem"];

  return (
    <Table headers={headers} className="[&_table]:min-w-[700px]">
      {metas.map((meta) => (
        <tr key={meta.id} className="hover:bg-slate-700/30 transition-colors">
          <td className="px-6 py-4">
            <div className="text-white font-semibold">{meta.titulo}</div>
            <div className="text-slate-400 text-xs mt-0.5">{meta.descricao}</div>
            {meta.indicador && (
              <div className="text-slate-500 text-xs mt-1 italic">
                Indicador: {meta.indicador}
              </div>
            )}
          </td>
          <td className="px-6 py-4 text-slate-300 text-sm whitespace-nowrap">
            {formatarData(meta.prazo)}
          </td>
          <td className="px-6 py-4 whitespace-nowrap">
            <PrioridadeMetaBadge prioridade={meta.prioridade} />
          </td>
          <td className="px-6 py-4 whitespace-nowrap">
            <StatusMetaBadge status={meta.status} />
          </td>
          <td className="px-6 py-4 text-slate-400 text-xs whitespace-nowrap">
            {meta.origem || "MANUAL"}
          </td>
        </tr>
      ))}
    </Table>
  );
}
