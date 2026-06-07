import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import { formatClassificacao } from "./avaliacaoUtils";

export default function ResultadoAvaliacao({ resultado, onReset }) {
  const avaliacao = resultado?.avaliacao;
  const perfil = resultado?.perfil_talento;
  const medias = resultado?.resultado_competencias;
  
  const colaboradorId = avaliacao?.colaborador_id;

  const formatMedia = (val) => {
    if (val === undefined || val === null) return "Não avaliado";
    return typeof val === "number" ? val.toFixed(2) : parseFloat(val).toFixed(2);
  };

  const getBadgeClass = (classificacao) => {
    const map = {
      ALTA_PERFORMANCE: "bg-emerald-500/10 text-emerald-400 border-emerald-500/25",
      ESPECIALISTA_TECNICO: "bg-blue-500/10 text-blue-400 border-blue-500/25",
      POTENCIAL_LIDER: "bg-indigo-500/10 text-indigo-400 border-indigo-500/25",
      TALENTO_EM_DESENVOLVIMENTO: "bg-amber-500/10 text-amber-400 border-amber-500/25",
      NECESSITA_DESENVOLVIMENTO: "bg-rose-500/10 text-rose-400 border-rose-500/25"
    };
    return map[classificacao] || "bg-slate-700/55 text-slate-300 border-slate-600/25";
  };

  const formatPotencialLideranca = (potencial) => {
    if (potencial === undefined || potencial === null) return "Não informado";
    if (typeof potencial === "boolean") {
      return potencial ? "Sim" : "Não";
    }
    const str = String(potencial).toLowerCase();
    if (str === "true" || str === "sim" || str === "yes") return "Sim";
    if (str === "false" || str === "não" || str === "no") return "Não";
    return potencial;
  };

  return (
    <div className="space-y-6">
      <div className="bg-indigo-600/10 border border-indigo-500/20 rounded-2xl p-6 flex flex-col md:flex-row items-center md:justify-between space-y-4 md:space-y-0">
        <div>
          <h3 className="text-lg font-bold text-white">Avaliação registrada com sucesso!</h3>
          <p className="text-slate-400 text-sm mt-1">
            Os dados foram processados e as notas de competências foram calculadas.
          </p>
        </div>
        <div className="text-sm font-semibold text-slate-300">
          ID da Avaliação: <span className="text-indigo-400">{avaliacao?.id ?? "Não informado"}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Medias Card */}
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <h3 className="text-base font-bold text-white mb-4 border-b border-slate-700 pb-2">
              Médias Calculadas
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center py-1.5 border-b border-slate-800">
                <span className="text-sm text-slate-400">Técnica</span>
                <span className="text-sm font-bold text-white">{formatMedia(medias?.media_tecnica)}</span>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-slate-800">
                <span className="text-sm text-slate-400">Comportamental</span>
                <span className="text-sm font-bold text-white">{formatMedia(medias?.media_comportamental)}</span>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-slate-800">
                <span className="text-sm text-slate-400">Liderança</span>
                <span className="text-sm font-bold text-white">{formatMedia(medias?.media_lideranca)}</span>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-slate-800">
                <span className="text-sm text-slate-400">Organizacional</span>
                <span className="text-sm font-bold text-white">{formatMedia(medias?.media_organizacional)}</span>
              </div>
              <div className="flex justify-between items-center pt-3 mt-1">
                <span className="text-sm font-bold text-slate-300">Média Geral</span>
                <span className="text-lg font-black text-indigo-400">{formatMedia(medias?.media_geral)}</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Perfil Card */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 mb-4 border-b border-slate-700">
              <div>
                <h3 className="text-base font-bold text-white">Classificação de Perfil de Talento</h3>
                <p className="text-slate-400 text-xs mt-0.5">Gerado pelas regras do domínio com base nas notas</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-black border uppercase tracking-wider ${getBadgeClass(perfil?.classificacao)}`}>
                {formatClassificacao(perfil?.classificacao)}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
              <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
                <span className="text-[10px] text-slate-400 font-bold uppercase block">Nível Técnico</span>
                <span className="text-sm font-bold text-white mt-1 block">
                  {perfil?.nivel_tecnico ?? "Não informado"}
                </span>
              </div>
              <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
                <span className="text-[10px] text-slate-400 font-bold uppercase block">Nível Comportamental</span>
                <span className="text-sm font-bold text-white mt-1 block">
                  {perfil?.nivel_comportamental ?? "Não informado"}
                </span>
              </div>
              <div className="bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
                <span className="text-[10px] text-slate-400 font-bold uppercase block">Potencial de Liderança</span>
                <span className="text-sm font-bold text-white mt-1 block">
                  {formatPotencialLideranca(perfil?.potencial_lideranca)}
                </span>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-1">Resumo do Perfil</h4>
                <p className="text-sm text-slate-300 bg-slate-800/30 p-3 rounded-lg border border-slate-700/30 leading-relaxed">
                  {perfil?.resumo ?? "Não informado"}
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* insights (Pontos Fortes, Pontos de Melhoria, Recomendacoes) */}
      <Card>
        <h3 className="text-base font-bold text-white mb-6 border-b border-slate-700 pb-2">
          Análise e Recomendações do Sistema
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Pontos Fortes */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-emerald-400 flex items-center space-x-1.5">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Pontos Fortes</span>
            </h4>
            <ul className="space-y-2">
              {perfil?.pontos_fortes && perfil.pontos_fortes.length > 0 ? (
                perfil.pontos_fortes.map((p, idx) => (
                  <li key={idx} className="text-slate-300 text-xs bg-slate-800/30 p-2.5 rounded-lg border border-slate-700/20 leading-relaxed">
                    {p}
                  </li>
                ))
              ) : (
                <li className="text-slate-500 text-xs italic">Nenhum ponto forte identificado.</li>
              )}
            </ul>
          </div>

          {/* Pontos de Melhoria */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-rose-400 flex items-center space-x-1.5">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>Pontos de Melhoria</span>
            </h4>
            <ul className="space-y-2">
              {perfil?.pontos_melhoria && perfil.pontos_melhoria.length > 0 ? (
                perfil.pontos_melhoria.map((p, idx) => (
                  <li key={idx} className="text-slate-300 text-xs bg-slate-800/30 p-2.5 rounded-lg border border-slate-700/20 leading-relaxed">
                    {p}
                  </li>
                ))
              ) : (
                <li className="text-slate-500 text-xs italic">Nenhum ponto de melhoria identificado.</li>
              )}
            </ul>
          </div>

          {/* Recomendacoes */}
          <div className="space-y-3">
            <h4 className="text-sm font-bold text-indigo-400 flex items-center space-x-1.5">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span>Recomendações de Desenvolvimento</span>
            </h4>
            <ul className="space-y-2">
              {perfil?.recomendacoes && perfil.recomendacoes.length > 0 ? (
                perfil.recomendacoes.map((p, idx) => (
                  <li key={idx} className="text-slate-300 text-xs bg-slate-800/30 p-2.5 rounded-lg border border-slate-700/20 leading-relaxed">
                    {p}
                  </li>
                ))
              ) : (
                <li className="text-slate-500 text-xs italic">Nenhuma recomendação gerada.</li>
              )}
            </ul>
          </div>
        </div>
      </Card>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-end gap-3 pt-4 border-t border-slate-800">
        <Button variant="secondary" onClick={onReset}>
          Registrar outra avaliação
        </Button>
        {colaboradorId && (
          <Link to={`/colaboradores/${colaboradorId}/evolucao`}>
            <Button variant="outline">
              Visualizar evolução do colaborador
            </Button>
          </Link>
        )}
        <Link to="/avaliacoes">
          <Button variant="primary">
            Voltar para Avaliações
          </Button>
        </Link>
      </div>
    </div>
  );
}
