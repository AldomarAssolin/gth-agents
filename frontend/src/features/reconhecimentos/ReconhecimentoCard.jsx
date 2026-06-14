import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import TipoReconhecimentoBadge from "./TipoReconhecimentoBadge";
import StatusReconhecimentoBadge from "./StatusReconhecimentoBadge";
import { formatarData } from "./reconhecimentosFormatters";

export default function ReconhecimentoCard({
  reconhecimento,
  currentUser,
  colaboradorNome = "",
  onCancelar,
}) {
  const isGestor = ["ADMIN", "RH", "LIDER"].includes(currentUser?.perfil);
  const registradorLabel =
    currentUser?.id === reconhecimento.registrado_por_id
      ? "Registrado por você"
      : `Registrado pelo usuário #${reconhecimento.registrado_por_id}`;

  const canceladorLabel =
    currentUser?.id === reconhecimento.cancelado_por_id
      ? "Cancelado por você"
      : `Cancelado pelo usuário #${reconhecimento.cancelado_por_id}`;

  return (
    <Card className="bg-slate-800/80 border border-slate-700/60 shadow-lg hover:border-slate-600/70 transition-all space-y-4">
      {/* Top badges and metadata */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-700/40 pb-3">
        <div className="flex items-center space-x-2">
          <TipoReconhecimentoBadge tipo={reconhecimento.tipo} />
          <StatusReconhecimentoBadge ativo={reconhecimento.ativo} />
        </div>
        <span className="text-xs text-slate-400 font-medium">
          {formatarData(reconhecimento.criado_em)}
        </span>
      </div>

      {/* Main details */}
      <div className="space-y-3">
        <div>
          <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Colaborador
          </span>
          <span className="text-white font-medium text-sm">
            {colaboradorNome || `Colaborador #${reconhecimento.colaborador_id}`}
          </span>
        </div>

        <div>
          <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Descrição
          </span>
          <p className="text-slate-200 text-sm mt-1 whitespace-pre-line leading-relaxed">
            {reconhecimento.descricao}
          </p>
        </div>

        <div>
          <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Evidência
          </span>
          <p className="text-slate-300 text-xs mt-1 italic whitespace-pre-line bg-slate-900/40 p-3 rounded-lg border border-slate-700/30">
            {reconhecimento.evidencia}
          </p>
        </div>

        {/* Audit footer */}
        <div className="text-xs text-slate-400 pt-2 border-t border-slate-700/40 flex items-center justify-between">
          <span>{registradorLabel}</span>
        </div>

        {/* Cancellation audit info */}
        {!reconhecimento.ativo && (
          <div className="bg-red-500/5 border border-red-500/10 rounded-lg p-3 mt-3 text-xs space-y-2">
            <div className="flex items-center justify-between font-semibold text-red-400">
              <span>{canceladorLabel}</span>
              <span>{formatarData(reconhecimento.cancelado_em)}</span>
            </div>
            {reconhecimento.motivo_cancelamento && (
              <div>
                <span className="text-slate-400 font-medium block">Motivo:</span>
                <p className="text-slate-300 mt-1">{reconhecimento.motivo_cancelamento}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Action button */}
      {isGestor && reconhecimento.ativo && onCancelar && (
        <div className="flex justify-end pt-2">
          <Button
            onClick={() => onCancelar(reconhecimento)}
            variant="secondary"
            className="text-xs py-1.5 px-3 hover:bg-red-600/10 hover:text-red-400 hover:border-red-600/30 transition-all"
          >
            Cancelar Reconhecimento
          </Button>
        </div>
      )}
    </Card>
  );
}
