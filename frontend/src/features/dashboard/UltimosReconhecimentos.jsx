import Card from "../../components/ui/Card";
import EmptyState from "../../components/ui/EmptyState";
import { formatDateTime } from "../../utils/format";

export default function UltimosReconhecimentos({ data }) {
  const reconhecimentos = data?.reconhecimentos?.ultimos ?? [];

  return (
    <Card className="flex flex-col h-full">
      <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
        <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5a2 2 0 10-2 2h2zm0 0L4 12m8 0l8-4M4 12l8 8m0-8L4 8" />
        </svg>
        <span>Últimos Reconhecimentos</span>
      </h3>

      {reconhecimentos.length === 0 ? (
        <div className="flex-1 flex flex-col justify-center">
          <EmptyState
            title="Nenhum reconhecimento registrado"
            message="Não há reconhecimentos de destaque ou técnicos registrados."
          />
        </div>
      ) : (
        <div className="divide-y divide-slate-700/60 overflow-hidden flex-1">
          {reconhecimentos.map((rec, index) => (
            <div key={rec.id ?? index} className="py-3.5 flex justify-between items-start space-x-4">
              <div className="space-y-1">
                <span className="text-xs font-semibold uppercase tracking-wider text-amber-400">
                  {rec.tipo ? rec.tipo.replace(/_/g, " ") : "RECONHECIMENTO"}
                </span>
                <p className="text-xs text-slate-400 font-medium">
                  Colaborador ID: {rec.colaborador_id ?? "N/A"}
                </p>
              </div>
              <div className="text-right">
                <span className="text-[10px] text-slate-500 font-semibold block">
                  {formatDateTime(rec.data_reconhecimento)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
