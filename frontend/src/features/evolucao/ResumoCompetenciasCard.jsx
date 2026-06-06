import Card from "../../components/ui/Card";
import { formatarMedia } from "./evolucaoFormatters";

export default function ResumoCompetenciasCard({ indicadores }) {
  const safeInd = indicadores || {};
  const totalAvaliacoes = safeInd.total_avaliacoes ?? 0;

  const mediaTecnicaStr = formatarMedia(safeInd.media_tecnica, totalAvaliacoes);
  const mediaComportamentalStr = formatarMedia(safeInd.media_comportamental, totalAvaliacoes);

  const renderProgress = (valStr) => {
    if (valStr === "Ainda não avaliado") return null;
    const numVal = parseFloat(valStr.replace(",", "."));
    if (isNaN(numVal)) return null;

    // Convert 1-5 scale to percentage
    const percent = Math.min(Math.max((numVal / 5) * 100, 0), 100);

    return (
      <div className="w-full bg-slate-800 rounded-full h-1.5 mt-3 overflow-hidden">
        <div
          className="bg-indigo-500 h-1.5 rounded-full"
          style={{ width: `${percent}%` }}
        ></div>
      </div>
    );
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card className="bg-slate-900 border-slate-800 p-5 flex flex-col justify-between relative overflow-hidden">
        <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-full blur-xl pointer-events-none"></div>
        <div>
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Média Técnica</span>
          <span className={`block font-bold mt-2 ${mediaTecnicaStr === "Ainda não avaliado" ? "text-slate-500 text-sm italic" : "text-white text-3xl"}`}>
            {mediaTecnicaStr}
          </span>
        </div>
        {renderProgress(mediaTecnicaStr)}
      </Card>

      <Card className="bg-slate-900 border-slate-800 p-5 flex flex-col justify-between relative overflow-hidden">
        <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-full blur-xl pointer-events-none"></div>
        <div>
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Média Comportamental</span>
          <span className={`block font-bold mt-2 ${mediaComportamentalStr === "Ainda não avaliado" ? "text-slate-500 text-sm italic" : "text-white text-3xl"}`}>
            {mediaComportamentalStr}
          </span>
        </div>
        {renderProgress(mediaComportamentalStr)}
      </Card>
    </div>
  );
}
