import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import { formatarDataBrasil } from "./evolucaoFormatters";

export default function FeedbacksResumo({ feedbacks: feedbacksProps }) {
  const feedbacks = Array.isArray(feedbacksProps) ? feedbacksProps : [];

  return (
    <Card className="bg-slate-900 border-slate-800">
      <div className="border-b border-slate-800 pb-4 mb-5 flex items-center justify-between">
        <div>
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Feedbacks Recebidos</span>
          <h3 className="text-lg font-bold text-white mt-1">Registros de Feedback</h3>
        </div>
        {feedbacks.length > 0 && (
          <Badge variant="info">
            {feedbacks.length} {feedbacks.length === 1 ? "Feedback" : "Feedbacks"}
          </Badge>
        )}
      </div>

      {feedbacks.length === 0 ? (
        <div className="py-8 text-center">
          <p className="text-slate-500 text-sm italic">Nenhum feedback registrado para este colaborador.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {feedbacks.map((f) => (
            <div
              key={f.id}
              className="p-5 bg-slate-800/20 border border-slate-800 rounded-xl space-y-4 hover:border-slate-700 transition-all duration-200"
            >
              {/* Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/60 pb-3">
                <span className="text-xs text-slate-400 font-semibold truncate">
                  Contexto: <strong className="text-slate-300">{f.contexto || "Geral"}</strong>
                </span>
                <div className="flex items-center gap-3 text-xs text-slate-500">
                  {f.autor && (
                    <span>
                      Autor: <strong className="text-indigo-400">{f.autor}</strong>
                    </span>
                  )}
                  <span>{formatarDataBrasil(f.data_feedback)}</span>
                </div>
              </div>

              {/* Grid content */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Ponto Positivo */}
                <div className="space-y-1">
                  <span className="block text-[10px] text-emerald-400 uppercase font-semibold tracking-wider">Pontos Positivos</span>
                  <p className="text-slate-300 text-xs leading-relaxed bg-slate-900/40 p-3 rounded-lg border border-slate-800/80">
                    {f.ponto_positivo || "Não registrado"}
                  </p>
                </div>

                {/* Ponto Melhoria */}
                <div className="space-y-1">
                  <span className="block text-[10px] text-amber-400 uppercase font-semibold tracking-wider">Pontos de Melhoria</span>
                  <p className="text-slate-300 text-xs leading-relaxed bg-slate-900/40 p-3 rounded-lg border border-slate-800/80">
                    {f.ponto_melhoria || "Não registrado"}
                  </p>
                </div>

                {/* Acao Recomendada */}
                <div className="space-y-1">
                  <span className="block text-[10px] text-indigo-400 uppercase font-semibold tracking-wider">Ações Recomendadas</span>
                  <p className="text-slate-300 text-xs leading-relaxed bg-slate-900/40 p-3 rounded-lg border border-slate-800/80">
                    {f.acao_recomendada || "Nenhuma ação recomendada"}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
