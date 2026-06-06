import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import { formatarDataBrasil, traduzirTipoAvaliacao } from "./evolucaoFormatters";

export default function AvaliacoesDetalhes({ avaliacoes: avaliacoesProps }) {
  const avaliacoes = Array.isArray(avaliacoesProps) ? avaliacoesProps : [];

  return (
    <Card className="bg-slate-900 border-slate-800">
      <div className="border-b border-slate-800 pb-4 mb-5">
        <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Avaliações Detalhadas</span>
        <h3 className="text-lg font-bold text-white mt-1">Competências e Notas</h3>
      </div>

      {avaliacoes.length === 0 ? (
        <div className="py-8 text-center">
          <p className="text-slate-500 text-sm italic">Nenhuma avaliação detalhada registrada.</p>
        </div>
      ) : (
        <div className="space-y-8">
          {avaliacoes.map((av, idx) => {
            const dateStr = av.data_avaliacao || av.criado_em;
            
            return (
              <div
                key={av.id || idx}
                className="border border-slate-800 rounded-xl p-5 bg-slate-800/20"
              >
                {/* Header of specific evaluation */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3 mb-4">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
                    <h4 className="font-semibold text-slate-200">
                      {traduzirTipoAvaliacao(av.tipo)}
                    </h4>
                  </div>
                  {dateStr && (
                    <span className="text-xs text-slate-500">
                      Realizada em: {formatarDataBrasil(dateStr)}
                    </span>
                  )}
                </div>

                {/* Items/Competencies evaluated */}
                {!av.itens || av.itens.length === 0 ? (
                  <p className="text-slate-500 text-xs italic">
                    Esta avaliação não possui notas ou itens registrados.
                  </p>
                ) : (
                  <div className="space-y-4">
                    {av.itens.map((item) => {
                      const comp = item.competencia || {};
                      const isTecnica = comp.tipo === "TECNICA";

                      return (
                        <div
                          key={item.id}
                          className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-3 bg-slate-900/50 border border-slate-800/80 rounded-lg"
                        >
                          <div className="min-w-0 flex-1">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-sm font-semibold text-white truncate">
                                {comp.nome || "Competência não identificada"}
                              </span>
                              <Badge variant={isTecnica ? "info" : "success"}>
                                {isTecnica ? "Técnica" : "Comportamental"}
                              </Badge>
                            </div>
                            {item.comentario && (
                              <p className="text-slate-400 text-xs mt-1 leading-relaxed italic">
                                "{item.comentario}"
                              </p>
                            )}
                          </div>
                          
                          <div className="flex items-center gap-1.5 shrink-0 self-end sm:self-center">
                            <span className="text-xs text-slate-500">Nota:</span>
                            <span className="text-base font-bold text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded-md border border-indigo-500/20">
                              {item.nota ?? 0}/5
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </Card>
  );
}
