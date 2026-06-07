import { Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import { useAuth } from "../features/auth/useAuth";

export default function AvaliacoesPage() {
  const { user } = useAuth();
  const canCreateAvaliacao = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <PageHeader
          title="Avaliações de Desempenho"
          description="Gestão de ciclos avaliativos, autoavaliações e avaliações de liderança"
        />
        {canCreateAvaliacao && (
          <Link to="/avaliacoes/nova" className="self-start sm:self-auto">
            <Button variant="primary">
              Nova Avaliação
            </Button>
          </Link>
        )}
      </div>

      <Card>
        <div className="max-w-2xl">
          <h2 className="text-xl font-bold text-white mb-2">Módulo de Avaliações de Competências</h2>
          <p className="text-slate-400 text-sm mb-6 leading-relaxed">
            Aqui você pode gerenciar, registrar e analisar as avaliações de desempenho dos colaboradores.
            O sistema calcula as médias das competências e utiliza inteligência artificial para traçar o perfil de talento, identificar pontos fortes, melhorias e sugerir recomendações para o Plano de Desenvolvimento Individual (PDI).
          </p>

          <div className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-6">
            <h3 className="text-base font-bold text-indigo-400 mb-2 flex items-center space-x-2">
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Listagem Geral Indisponível</span>
            </h3>
            <p className="text-slate-300 text-sm leading-relaxed">
              A listagem histórica e a consulta de avaliações passadas não estão disponíveis no sistema.
              {canCreateAvaliacao ? (
                <> Para registrar uma nova avaliação e obter o diagnóstico de competências em tempo real, clique no botão <strong>Nova Avaliação</strong> acima.</>
              ) : (
                <> As funcionalidades de visualização de avaliações serão liberadas pelo time de Gente & Gestão em breve.</>
              )}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
