import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";

export default function FeedbacksPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Feedbacks"
        description="Troca de feedbacks constantes entre membros da organização e gestores"
      />
      <Card>
        <h2 className="text-xl font-bold text-white mb-2">Central de Feedbacks</h2>
        <p className="text-slate-400 text-sm mb-6">Solicite ou envie feedbacks estruturados para seus colegas de trabalho.</p>
        
        <EmptyState
          title="Nenhum feedback recebido"
          message="Seu histórico de feedbacks recebidos ou enviados está vazio no momento."
        />
      </Card>
    </div>
  );
}
