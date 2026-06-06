import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import { formatarDataBrasil } from "./evolucaoFormatters";

export default function ReconhecimentosResumo({ reconhecimentos: reconhecimentosProps }) {
  const reconhecimentos = Array.isArray(reconhecimentosProps)
    ? reconhecimentosProps.filter((r) => r.ativo !== false)
    : [];

  const getTipoLabel = (tipo) => {
    const mapa = {
      DESTAQUE: "Destaque",
      EVOLUCAO_TECNICA: "Evolução Técnica",
      EVOLUCAO_COMPORTAMENTAL: "Evolução Comportamental",
      INICIATIVA: "Iniciativa"
    };
    return mapa[tipo] || tipo || "Reconhecimento";
  };

  return (
    <Card className="bg-slate-900 border-slate-800">
      <div className="border-b border-slate-800 pb-4 mb-5 flex items-center justify-between">
        <div>
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Reconhecimentos</span>
          <h3 className="text-lg font-bold text-white mt-1">Conquistas e Destaques</h3>
        </div>
        {reconhecimentos.length > 0 && (
          <Badge variant="success">
            {reconhecimentos.length} {reconhecimentos.length === 1 ? "Ativo" : "Ativos"}
          </Badge>
        )}
      </div>

      {reconhecimentos.length === 0 ? (
        <div className="py-8 text-center">
          <p className="text-slate-500 text-sm italic">Nenhum reconhecimento registrado.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {reconhecimentos.map((r) => (
            <div
              key={r.id}
              className="p-4 bg-slate-800/20 border border-slate-800 rounded-xl hover:border-slate-700 transition-all duration-200"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/50 pb-2 mb-3">
                <span className="text-sm font-semibold text-indigo-400">
                  {getTipoLabel(r.tipo)}
                </span>
                <span className="text-xs text-slate-500">
                  {formatarDataBrasil(r.data_reconhecimento)}
                </span>
              </div>
              
              <div className="space-y-2.5">
                <p className="text-slate-200 text-sm leading-relaxed">
                  {r.descricao}
                </p>
                {r.evidencia && (
                  <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800/80">
                    <span className="block text-[10px] text-slate-500 font-semibold uppercase tracking-wider mb-1">
                      Evidência
                    </span>
                    <p className="text-slate-300 text-xs leading-relaxed italic">
                      "{r.evidencia}"
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
