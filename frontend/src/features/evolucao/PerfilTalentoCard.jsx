import Card from "../../components/ui/Card";
import {

  formatarDataBrasil,
  traduzirClassificacao,
  traduzirNivel,
  traduzirOrigemPDI
} from "./evolucaoFormatters";

export default function PerfilTalentoCard({ perfilAtual }) {
  // If perfilAtual is null or undefined
  if (!perfilAtual) {
    return (
      <Card className="bg-slate-900 border-slate-800 p-8 flex flex-col items-center justify-center text-center">
        <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 mb-4">
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <h3 className="text-white font-semibold text-base">Sem Perfil de Talento</h3>
        <p className="text-slate-400 text-sm mt-1 max-w-sm">
          Este colaborador ainda não possui um perfil de talento gerado pelo sistema.
        </p>
      </Card>
    );
  }

  const renderLista = (titulo, itens, mensagemVazia, listColorClass) => {
    const validItens = Array.isArray(itens) ? itens.filter(Boolean) : [];

    return (
      <div className="flex flex-col space-y-2">
        <h4 className="text-sm font-semibold text-slate-200 tracking-wide uppercase text-xs">{titulo}</h4>
        {validItens.length === 0 ? (
          <p className="text-slate-500 text-sm italic">{mensagemVazia}</p>
        ) : (
          <ul className="space-y-2">
            {validItens.map((item, idx) => (
              <li key={idx} className="flex items-start space-x-2 text-slate-300 text-sm leading-relaxed">
                <span className={`w-1.5 h-1.5 rounded-full mt-1.5 shrink-0 ${listColorClass}`}></span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    );
  };

  return (
    <Card className="relative overflow-hidden bg-slate-900 border-slate-800">
      <div className="absolute top-0 right-0 w-48 h-48 bg-indigo-500/5 rounded-full blur-3xl pointer-events-none"></div>
      
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 mb-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider block">Perfil de Talento Atual</span>
          <h3 className="text-xl font-bold text-white mt-1">
            {traduzirClassificacao(perfilAtual.classificacao)}
          </h3>
        </div>
        <div className="flex flex-col sm:items-end text-xs text-slate-400">
          <span>Origem: <strong className="text-indigo-400">{traduzirOrigemPDI(perfilAtual.origem)}</strong></span>
          <span className="mt-0.5">Gerado em: <strong>{formatarDataBrasil(perfilAtual.criado_em || perfilAtual.data_geracao)}</strong></span>
        </div>
      </div>

      {/* Resumo */}
      {perfilAtual.resumo && (
        <div className="mb-6 p-4 bg-slate-800/30 border border-slate-800/80 rounded-xl">
          <span className="block text-[11px] text-slate-500 font-semibold uppercase tracking-wider mb-1">Resumo do Perfil</span>
          <p className="text-slate-300 text-sm leading-relaxed">{perfilAtual.resumo}</p>
        </div>
      )}

      {/* Niveis */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="p-4 bg-slate-800/50 border border-slate-800 rounded-xl flex flex-col justify-between">
          <span className="text-xs text-slate-400 font-medium">Nível Técnico</span>
          <span className="text-lg font-semibold text-white mt-2">
            {traduzirNivel(perfilAtual.nivel_tecnico)}
          </span>
        </div>
        <div className="p-4 bg-slate-800/50 border border-slate-800 rounded-xl flex flex-col justify-between">
          <span className="text-xs text-slate-400 font-medium">Nível Comportamental</span>
          <span className="text-lg font-semibold text-white mt-2">
            {traduzirNivel(perfilAtual.nivel_comportamental)}
          </span>
        </div>
        <div className="p-4 bg-slate-800/50 border border-slate-800 rounded-xl flex flex-col justify-between">
          <span className="text-xs text-slate-400 font-medium">Potencial de Liderança</span>
          <span className="text-lg font-semibold text-white mt-2">
            {traduzirNivel(perfilAtual.potencial_lideranca)}
          </span>
        </div>
      </div>

      {/* Listas: Pontos Fortes, Melhoria, Recomendacoes */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2 border-t border-slate-800/60">
        {renderLista(
          "Pontos Fortes",
          perfilAtual.pontos_fortes,
          "Nenhum ponto forte registrado.",
          "bg-emerald-500"
        )}
        {renderLista(
          "Pontos de Melhoria",
          perfilAtual.pontos_melhoria,
          "Nenhum ponto de melhoria registrado.",
          "bg-amber-500"
        )}
        {renderLista(
          "Recomendações",
          perfilAtual.recomendacoes,
          "Nenhuma recomendação disponível.",
          "bg-indigo-500"
        )}
      </div>
    </Card>
  );
}
