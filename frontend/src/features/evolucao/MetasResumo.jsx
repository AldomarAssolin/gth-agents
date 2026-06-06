import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import { formatarDataBrasil, traduzirStatus, traduzirPrioridade } from "./evolucaoFormatters";

export default function MetasResumo({ metas: metasProps }) {
  const metas = Array.isArray(metasProps) ? metasProps : [];

  const getStatusVariant = (status) => {
    switch (status) {
      case "CONCLUIDA":
      case "CONCLUIDO":
        return "success";
      case "ATRASADA":
      case "ATRASADO":
        return "danger";
      case "PENDENTE":
        return "warning";
      default:
        return "secondary";
    }
  };

  const getPrioridadeVariant = (prioridade) => {
    switch (prioridade) {
      case "CRITICA":
        return "danger";
      case "ALTA":
        return "warning";
      case "MEDIA":
        return "info";
      default:
        return "secondary";
    }
  };

  return (
    <Card className="bg-slate-900 border-slate-800">
      <div className="border-b border-slate-800 pb-4 mb-5 flex items-center justify-between">
        <div>
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Metas Individuais</span>
          <h3 className="text-lg font-bold text-white mt-1">Acompanhamento de Metas</h3>
        </div>
        {metas.length > 0 && (
          <Badge variant="info">
            {metas.length} {metas.length === 1 ? "Meta" : "Metas"}
          </Badge>
        )}
      </div>

      {metas.length === 0 ? (
        <div className="py-8 text-center">
          <p className="text-slate-500 text-sm italic">Nenhuma meta registrada para este colaborador.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {metas.map((meta) => {
            const isAtrasada = meta.status === "ATRASADA" || meta.status === "ATRASADO";
            
            return (
              <div
                key={meta.id}
                className={`p-4 rounded-xl border transition-all duration-200 ${
                  isAtrasada
                    ? "bg-red-500/[0.02] border-red-500/30 hover:border-red-500/50"
                    : "bg-slate-800/20 border-slate-800 hover:border-slate-700"
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm font-semibold text-slate-200 truncate">
                        {meta.titulo}
                      </span>
                      {isAtrasada && (
                        <span className="inline-flex items-center text-[10px] font-bold text-red-400 uppercase tracking-wider bg-red-500/10 px-2 py-0.5 rounded-md border border-red-500/20 animate-pulse">
                          Atrasada
                        </span>
                      )}
                    </div>
                    {meta.descricao && (
                      <p className="text-slate-400 text-xs mt-1 truncate">
                        {meta.descricao}
                      </p>
                    )}
                  </div>
                  
                  <div className="flex items-center gap-2 flex-wrap sm:justify-end">
                    <Badge variant={getPrioridadeVariant(meta.prioridade)}>
                      {traduzirPrioridade(meta.prioridade)}
                    </Badge>
                    <Badge variant={getStatusVariant(meta.status)}>
                      {traduzirStatus(meta.status)}
                    </Badge>
                  </div>
                </div>

                <div className="flex items-center gap-1.5 mt-3 pt-3 border-t border-slate-800/60 text-xs text-slate-500">
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>Prazo: {formatarDataBrasil(meta.prazo)}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </Card>
  );
}
