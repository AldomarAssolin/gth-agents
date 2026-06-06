import Card from "../../components/ui/Card";
import EmptyState from "../../components/ui/EmptyState";
import { formatDateTime } from "../../utils/format";

export default function UltimosFeedbacks({ data }) {
  const feedbacks = data?.feedbacks?.ultimos ?? [];

  return (
    <Card className="flex flex-col h-full">
      <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
        <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
        </svg>
        <span>Últimos Feedbacks</span>
      </h3>

      {feedbacks.length === 0 ? (
        <div className="flex-1 flex flex-col justify-center">
          <EmptyState
            title="Nenhum feedback registrado"
            message="Não há histórico de feedbacks recentes cadastrados."
          />
        </div>
      ) : (
        <div className="divide-y divide-slate-700/60 overflow-hidden flex-1">
          {feedbacks.map((fb, index) => (
            <div key={fb.id ?? index} className="py-3.5 flex flex-col space-y-1.5">
              <div className="flex justify-between items-start space-x-4">
                <span className="text-xs font-semibold text-slate-300 leading-normal line-clamp-2">
                  {fb.contexto || "Sem descrição"}
                </span>
                <span className="text-[10px] text-slate-500 font-semibold shrink-0">
                  {formatDateTime(fb.data_feedback)}
                </span>
              </div>
              <p className="text-[10px] text-slate-500 font-bold">
                COLABORADOR ID: {fb.colaborador_id ?? "N/A"}
              </p>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
