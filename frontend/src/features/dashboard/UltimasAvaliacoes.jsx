import Card from "../../components/ui/Card";
import EmptyState from "../../components/ui/EmptyState";
import { formatDateTime } from "../../utils/format";

export default function UltimasAvaliacoes({ data }) {
  const avaliacoes = data?.avaliacoes?.ultimas ?? [];

  return (
    <Card className="flex flex-col h-full">
      <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
        <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        <span>Últimas Avaliações</span>
      </h3>

      {avaliacoes.length === 0 ? (
        <div className="flex-1 flex flex-col justify-center">
          <EmptyState
            title="Nenhuma avaliação registrada"
            message="Não há avaliações concluídas ou pendentes no momento."
          />
        </div>
      ) : (
        <div className="divide-y divide-slate-700/60 overflow-hidden flex-1">
          {avaliacoes.map((av, index) => (
            <div key={av.id ?? index} className="py-3.5 flex justify-between items-start space-x-4">
              <div className="space-y-1">
                <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">
                  {av.tipo ? av.tipo.replace(/_/g, " ") : "AVALIAÇÃO"}
                </span>
                <p className="text-xs text-slate-400 font-medium">
                  Colaborador ID: {av.colaborador_id ?? "N/A"}
                </p>
              </div>
              <div className="text-right">
                <span className="text-[10px] text-slate-500 font-semibold block">
                  {formatDateTime(av.data_avaliacao)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
