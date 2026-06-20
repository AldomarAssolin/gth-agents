import Card from "../../components/ui/Card";
import { formatarData } from "./feedbacksFormatters";

export default function FeedbackCard({
  feedback,
  currentUser,
  colaboradorNome = "",
}) {
  const dataExibicao = feedback.data_feedback || feedback.criado_em;
  const autorLabel = feedback.autor_id
    ? currentUser?.id === feedback.autor_id
      ? "Registrado por você"
      : `Registrado pelo usuário #${feedback.autor_id}`
    : "Autor não especificado";

  return (
    <Card className="bg-slate-800/80 border border-slate-700/60 shadow-lg hover:border-slate-600/70 transition-all space-y-4">
      {/* Top Header metadata */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-700/40 pb-3">
        <div className="space-y-0.5">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">
            Contexto: <strong className="text-slate-200">{feedback.contexto || "Geral"}</strong>
          </span>
          {colaboradorNome && (
            <span className="text-xs text-indigo-400 font-medium block">
              Colaborador: {colaboradorNome}
            </span>
          )}
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400 font-medium">
            {formatarData(dataExibicao)}
          </span>
        </div>
      </div>

      {/* Main feedback content blocks */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Ponto Positivo */}
        <div className="space-y-1">
          <span className="block text-[10px] text-emerald-400 uppercase font-semibold tracking-wider">
            Pontos Positivos
          </span>
          <p className="text-slate-200 text-xs leading-relaxed bg-slate-900/40 p-3 rounded-lg border border-slate-700/30 min-h-[70px] whitespace-pre-line">
            {feedback.ponto_positivo}
          </p>
        </div>

        {/* Ponto Melhoria */}
        <div className="space-y-1">
          <span className="block text-[10px] text-amber-400 uppercase font-semibold tracking-wider">
            Pontos de Melhoria
          </span>
          <p className="text-slate-200 text-xs leading-relaxed bg-slate-900/40 p-3 rounded-lg border border-slate-700/30 min-h-[70px] whitespace-pre-line">
            {feedback.ponto_melhoria || "Não registrado"}
          </p>
        </div>

        {/* Acao Recomendada */}
        <div className="space-y-1">
          <span className="block text-[10px] text-indigo-400 uppercase font-semibold tracking-wider">
            Ações Recomendadas
          </span>
          <p className="text-slate-200 text-xs leading-relaxed bg-slate-900/40 p-3 rounded-lg border border-slate-700/30 min-h-[70px] whitespace-pre-line">
            {feedback.acao_recomendada}
          </p>
        </div>
      </div>

      {/* Audit footer */}
      <div className="text-[11px] text-slate-400 pt-2 border-t border-slate-700/40 flex items-center justify-between">
        <span>{autorLabel}</span>
        <span className="bg-slate-700/40 text-slate-400 px-2 py-0.5 rounded text-[10px] uppercase font-semibold">
          {feedback.origem || "MANUAL"}
        </span>
      </div>
    </Card>
  );
}
