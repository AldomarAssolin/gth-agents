import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import { formatarDataBrasil, traduzirStatus, traduzirOrigemPDI } from "./evolucaoFormatters";

export default function PDISResumo({ pdis: pdisProps }) {
  const pdis = Array.isArray(pdisProps) ? pdisProps : [];

  const getStatusVariant = (status) => {
    switch (status) {
      case "ATIVO":
        return "info";
      case "CONCLUIDO":
      case "CONCLUIDA":
        return "success";
      case "CANCELADO":
      case "CANCELADA":
        return "danger";
      default:
        return "secondary";
    }
  };

  return (
    <Card className="bg-slate-900 border-slate-800">
      <div className="border-b border-slate-800 pb-4 mb-5 flex items-center justify-between">
        <div>
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Planos de Desenvolvimento</span>
          <h3 className="text-lg font-bold text-white mt-1">PDIs</h3>
        </div>
        {pdis.length > 0 && (
          <Badge variant="info">
            {pdis.length} {pdis.length === 1 ? "PDI" : "PDIs"}
          </Badge>
        )}
      </div>

      {pdis.length === 0 ? (
        <div className="py-8 text-center">
          <p className="text-slate-500 text-sm italic">Nenhum PDI registrado para este colaborador.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {pdis.map((pdi) => (
            <div
              key={pdi.id}
              className="p-4 bg-slate-800/20 border border-slate-800 hover:border-slate-700 rounded-xl transition-all duration-200"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <h4 className="text-sm font-semibold text-slate-200 truncate">
                    {pdi.titulo}
                  </h4>
                  {pdi.descricao && (
                    <p className="text-slate-400 text-xs mt-1 truncate">
                      {pdi.descricao}
                    </p>
                  )}
                </div>
                
                <div className="flex items-center gap-2 flex-wrap sm:justify-end">
                  <span className="text-xs text-slate-500">
                    Origem: <strong className="text-slate-400">{traduzirOrigemPDI(pdi.origem)}</strong>
                  </span>
                  <Badge variant={getStatusVariant(pdi.status)}>
                    {traduzirStatus(pdi.status)}
                  </Badge>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row sm:items-center gap-4 mt-3 pt-3 border-t border-slate-800/60 text-xs text-slate-500">
                <div className="flex items-center gap-1.5">
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>Início: {formatarDataBrasil(pdi.data_inicio)}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>Fim: {formatarDataBrasil(pdi.data_fim)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
