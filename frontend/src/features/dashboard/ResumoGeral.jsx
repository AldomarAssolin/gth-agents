import DashboardCard from "./DashboardCard";
import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";

export default function ResumoGeral({ data }) {
  const resumo = data?.resumo_geral ?? {};
  const metas = data?.metas ?? {};
  const pdis = data?.pdis ?? {};
  const reconhecimentos = data?.reconhecimentos ?? {};

  // Extract counts safely using nullish coalescing
  const totalColab = resumo.total_colaboradores ?? 0;
  const ativosColab = resumo.colaboradores_ativos ?? 0;
  const inativosColab = resumo.colaboradores_inativos ?? 0;

  const totalAvaliacoes = resumo.total_avaliacoes ?? 0;
  const totalFeedbacks = resumo.total_feedbacks ?? 0;
  const totalInteractions = totalAvaliacoes + totalFeedbacks;

  const pdisAtivos = pdis.ativos ?? 0;
  const pdisRascunho = pdis.rascunho ?? 0;
  const pdisConcluidos = pdis.concluidos ?? 0;
  const pdisCancelados = pdis.cancelados ?? 0;

  const recsAtivos = reconhecimentos.ativos ?? 0;
  const recsCancelados = reconhecimentos.cancelados ?? 0;

  // Meta counts
  const metasPendentes = metas.pendentes ?? 0;
  const metasEmAndamento = metas.em_andamento ?? 0;
  const metasConcluidas = metas.concluidas ?? 0;
  const metasAtrasadas = metas.atrasadas ?? 0;
  const metasCanceladas = metas.canceladas ?? 0;

  return (
    <div className="space-y-6">
      {/* Primeiras Metricas em Destaque */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
        <DashboardCard
          title="Total de Colaboradores"
          value={totalColab}
          footer={`${ativosColab} ativos • ${inativosColab} inativos`}
          valueClassName="text-white"
          icon={
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          }
        />

        <DashboardCard
          title="Avaliações & Feedbacks"
          value={totalInteractions}
          footer={`${totalAvaliacoes} avaliações • ${totalFeedbacks} feedbacks`}
          valueClassName="text-indigo-400"
          icon={
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          }
        />

        <DashboardCard
          title="PDIs Ativos"
          value={pdisAtivos}
          footer={`${pdisRascunho} rascunhos • ${pdisConcluidos} concluídos`}
          valueClassName="text-emerald-400"
          icon={
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          }
        />

        <DashboardCard
          title="Reconhecimentos Ativos"
          value={recsAtivos}
          footer={`${recsCancelados} cancelados`}
          valueClassName="text-amber-400"
          icon={
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
            </svg>
          }
        />
      </div>

      {/* Detalhamento de Status de Metas e PDIs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Metas Status */}
        <Card className="flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
              <svg className="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span>Situação das Metas</span>
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Pendentes</span>
                <Badge variant="info">{metasPendentes}</Badge>
              </div>
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Em Andamento</span>
                <Badge variant="warning">{metasEmAndamento}</Badge>
              </div>
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Concluídas</span>
                <Badge variant="success">{metasConcluidas}</Badge>
              </div>
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Atrasadas</span>
                <Badge variant="danger">{metasAtrasadas}</Badge>
              </div>
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40 col-span-2 sm:col-span-1">
                <span className="text-xs text-slate-400 font-medium mb-1">Canceladas</span>
                <Badge variant="secondary">{metasCanceladas}</Badge>
              </div>
            </div>
          </div>
        </Card>

        {/* PDIs Status */}
        <Card className="flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
              <svg className="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.168.477 4 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.168.477-4 1.253" />
              </svg>
              <span>Planos de Desenvolvimento (PDI)</span>
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Rascunho</span>
                <Badge variant="secondary">{pdisRascunho}</Badge>
              </div>
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Ativos</span>
                <Badge variant="info">{pdisAtivos}</Badge>
              </div>
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Concluídos</span>
                <Badge variant="success">{pdisConcluidos}</Badge>
              </div>
              <div className="flex flex-col items-center p-3 bg-slate-700/30 rounded-lg text-center border border-slate-700/40">
                <span className="text-xs text-slate-400 font-medium mb-1">Cancelados</span>
                <Badge variant="danger">{pdisCancelados}</Badge>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
