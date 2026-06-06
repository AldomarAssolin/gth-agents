import Card from "../../components/ui/Card";

export default function IndicadoresEvolucao({ indicadores }) {
  const safeInd = indicadores || {};

  const itens = [
    {
      label: "Avaliações",
      value: safeInd.total_avaliacoes ?? 0,
      icon: (
        <svg className="w-5 h-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    {
      label: "Feedbacks",
      value: safeInd.total_feedbacks ?? 0,
      icon: (
        <svg className="w-5 h-5 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      )
    },
    {
      label: "PDIs Ativos",
      value: safeInd.pdis_ativos ?? 0,
      icon: (
        <svg className="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      )
    },
    {
      label: "Reconhecimentos",
      value: safeInd.reconhecimentos ?? 0,
      icon: (
        <svg className="w-5 h-5 text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
        </svg>
      )
    },
    {
      label: "Metas Concluídas",
      value: `${safeInd.metas_concluidas ?? 0}/${safeInd.total_metas ?? 0}`,
      icon: (
        <svg className="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
      )
    },
    {
      label: "Metas Atrasadas",
      value: safeInd.metas_atrasadas ?? 0,
      icon: (
        <svg className="w-5 h-5 text-rose-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      ),
      highlight: (safeInd.metas_atrasadas ?? 0) > 0
    }
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-6 gap-4">
      {itens.map((item, idx) => (
        <Card
          key={idx}
          className={`p-4 bg-slate-900 border-slate-800 flex flex-col justify-between transition-all duration-200 hover:border-slate-700 ${
            item.highlight ? "ring-1 ring-red-500/30 bg-red-500/[0.02]" : ""
          }`}
        >
          <div className="flex items-center justify-between gap-2">
            <span className="text-slate-400 font-medium text-xs truncate">{item.label}</span>
            <div className="shrink-0">{item.icon}</div>
          </div>
          <div className="mt-3">
            <span className="text-xl font-bold text-white tracking-tight">{item.value}</span>
          </div>
        </Card>
      ))}
    </div>
  );
}
