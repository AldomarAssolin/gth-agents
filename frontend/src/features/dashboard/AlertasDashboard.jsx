import Card from "../../components/ui/Card";

export default function AlertasDashboard({ data }) {
  const alertas = data?.alertas ?? {};

  const metasAtrasadas = alertas.metas_atrasadas ?? 0;
  const pdisAtivos = alertas.pdis_ativos ?? 0;
  const colabSemAvaliacao = alertas.colaboradores_sem_avaliacao ?? 0;
  const colabSemPerfil = alertas.colaboradores_sem_perfil ?? 0;

  const activeAlerts = [];

  if (metasAtrasadas > 0) {
    activeAlerts.push({
      id: "metas_atrasadas",
      type: "danger",
      text: `${metasAtrasadas} ${metasAtrasadas === 1 ? "meta está atrasada" : "metas estão atrasadas"}.`,
      icon: (
        <svg className="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      ),
    });
  }

  if (colabSemAvaliacao > 0) {
    activeAlerts.push({
      id: "colab_sem_avaliacao",
      type: "warning",
      text: `${colabSemAvaliacao} ${colabSemAvaliacao === 1 ? "colaborador está sem avaliação" : "colaboradores estão sem avaliação"}.`,
      icon: (
        <svg className="h-5 w-5 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
    });
  }

  if (colabSemPerfil > 0) {
    activeAlerts.push({
      id: "colab_sem_perfil",
      type: "warning",
      text: `${colabSemPerfil} ${colabSemPerfil === 1 ? "colaborador não possui perfil de talento" : "colaboradores não possuem perfil de talento"}.`,
      icon: (
        <svg className="h-5 w-5 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
    });
  }

  if (pdisAtivos > 0) {
    activeAlerts.push({
      id: "pdis_ativos",
      type: "info",
      text: `${pdisAtivos} ${pdisAtivos === 1 ? "Plano de Desenvolvimento (PDI) ativo" : "Planos de Desenvolvimento (PDI) ativos"} em andamento.`,
      icon: (
        <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    });
  }

  return (
    <Card>
      <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
        <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <span>Alertas Críticos</span>
      </h3>

      {activeAlerts.length === 0 ? (
        <div className="flex items-center space-x-3 p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-400 text-sm font-semibold">
          <svg className="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Nenhum alerta crítico no momento.</span>
        </div>
      ) : (
        <div className="space-y-3">
          {activeAlerts.map((alert) => {
            const bgBorderColors = {
              danger: "bg-red-500/10 border-red-500/25 text-red-300",
              warning: "bg-amber-500/10 border-amber-500/25 text-amber-300",
              info: "bg-indigo-500/10 border-indigo-500/25 text-indigo-300",
            };
            const theme = bgBorderColors[alert.type] || bgBorderColors.info;

            return (
              <div
                key={alert.id}
                className={`flex items-start space-x-3 p-3.5 border rounded-lg text-xs font-medium ${theme}`}
              >
                <div className="shrink-0">{alert.icon}</div>
                <div className="leading-relaxed">{alert.text}</div>
              </div>
            );
          })}
        </div>
      )}
    </Card>
  );
}
