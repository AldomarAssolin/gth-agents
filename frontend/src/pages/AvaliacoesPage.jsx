import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";

export default function AvaliacoesPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Avaliações de Desempenho"
        description="Gestão de ciclos avaliativos, autoavaliações e avaliações liderança"
      />
      <Card>
        <h2 className="text-xl font-bold text-white mb-2">Painel de Avaliações</h2>
        <p className="text-slate-400 text-sm mb-6">Acompanhe os ciclos e o progresso das avaliações da organização.</p>
        
        <EmptyState
          title="Nenhum ciclo de avaliação ativo"
          message="Os ciclos de avaliação de desempenho programados aparecerão aqui assim que forem abertos pelo time de Gente & Gestão."
        />
      </Card>
    </div>
  );
}
