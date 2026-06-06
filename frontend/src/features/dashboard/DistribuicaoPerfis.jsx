import Card from "../../components/ui/Card";

const perfilLabels = {
  ALTA_PERFORMANCE: "Alta performance",
  POTENCIAL_LIDER: "Potencial líder",
  ESPECIALISTA_TECNICO: "Especialista técnico",
  TALENTO_EM_DESENVOLVIMENTO: "Talento em desenvolvimento",
  NECESSITA_DESENVOLVIMENTO: "Necessita desenvolvimento",
  SEM_PERFIL: "Sem perfil",
};

const fixedOrder = [
  "ALTA_PERFORMANCE",
  "POTENCIAL_LIDER",
  "ESPECIALISTA_TECNICO",
  "TALENTO_EM_DESENVOLVIMENTO",
  "NECESSITA_DESENVOLVIMENTO",
  "SEM_PERFIL",
];

// Curated tailwind color classes for visual elegance
const barColors = {
  ALTA_PERFORMANCE: "bg-indigo-500",
  POTENCIAL_LIDER: "bg-blue-500",
  ESPECIALISTA_TECNICO: "bg-emerald-500",
  TALENTO_EM_DESENVOLVIMENTO: "bg-amber-500",
  NECESSITA_DESENVOLVIMENTO: "bg-red-500",
  SEM_PERFIL: "bg-slate-500",
};

export default function DistribuicaoPerfis({ data }) {
  const perfis = data?.perfis_talento ?? {};
  
  // Calculate total, ensuring default of 0 is handled
  const total = fixedOrder.reduce((sum, key) => sum + (perfis[key] ?? 0), 0);

  return (
    <Card>
      <h3 className="text-base font-bold text-white mb-6 flex items-center space-x-2">
        <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z" />
        </svg>
        <span>Distribuição dos Perfis de Talento</span>
      </h3>

      <div className="space-y-4">
        {fixedOrder.map((key) => {
          const count = perfis[key] ?? 0;
          const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
          const label = perfilLabels[key] || key;
          const colorClass = barColors[key] || "bg-indigo-500";

          return (
            <div key={key} className="space-y-1.5">
              <div className="flex justify-between text-xs font-semibold">
                <span className="text-slate-300">{label}</span>
                <span className="text-slate-400">
                  {count} ({percentage}%)
                </span>
              </div>
              <div className="w-full bg-slate-700/50 rounded-full h-2 overflow-hidden border border-slate-700/35">
                <div
                  className={`${colorClass} h-2 rounded-full transition-all duration-500`}
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
