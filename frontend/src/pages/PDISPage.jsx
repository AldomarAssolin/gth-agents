import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";

export default function PDISPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="PDI (Plano de Desenvolvimento Individual)"
        description="Planejamento de carreira, competências técnicas e comportamentais"
      />
      <Card>
        <h2 className="text-xl font-bold text-white mb-2">Seu Plano de Desenvolvimento</h2>
        <p className="text-slate-400 text-sm mb-6">Ações de treinamento, mentoria e desenvolvimento focados no seu crescimento profissional.</p>
        
        <EmptyState
          title="Sem planos de desenvolvimento criados"
          message="Para iniciar a trilha de desenvolvimento, alinhe seus objetivos profissionais com seu gestor e crie um novo plano."
        />
      </Card>
    </div>
  );
}
