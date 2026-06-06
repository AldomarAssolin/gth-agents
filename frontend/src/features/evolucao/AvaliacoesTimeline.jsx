import Card from "../../components/ui/Card";
import { formatarDataBrasil, traduzirTipoAvaliacao } from "./evolucaoFormatters";

export default function AvaliacoesTimeline({ ultimasAvaliacoes }) {
  const avaliacoes = Array.isArray(ultimasAvaliacoes) ? ultimasAvaliacoes : [];

  return (
    <Card className="bg-slate-900 border-slate-800">
      <div className="border-b border-slate-800 pb-4 mb-5">
        <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Últimas Avaliações</span>
        <h3 className="text-lg font-bold text-white mt-1">Histórico Resumido</h3>
      </div>

      {avaliacoes.length === 0 ? (
        <div className="py-8 text-center">
          <p className="text-slate-500 text-sm italic">Nenhuma avaliação recente registrada.</p>
        </div>
      ) : (
        <div className="relative pl-6 border-l border-slate-800 space-y-6 ml-2 py-2">
          {avaliacoes.map((av) => (
            <div key={av.id} className="relative group">
              {/* Dot */}
              <div className="absolute -left-[31px] top-1.5 w-2.5 h-2.5 rounded-full bg-indigo-500 border border-slate-900 group-hover:scale-125 transition-transform duration-200"></div>
              
              <div>
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                  <h4 className="text-sm font-semibold text-white">
                    {traduzirTipoAvaliacao(av.tipo)}
                  </h4>
                  <span className="text-xs text-slate-500 font-medium">
                    {formatarDataBrasil(av.data_avaliacao)}
                  </span>
                </div>
                {av.observacao_geral ? (
                  <p className="text-slate-400 text-xs mt-1.5 leading-relaxed bg-slate-800/35 p-3 rounded-lg border border-slate-800/60">
                    {av.observacao_geral}
                  </p>
                ) : (
                  <p className="text-slate-500 text-xs mt-1 italic">
                    Sem observações gerais.
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
