import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";

export default function ReconhecimentosPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Reconhecimentos"
        description="Elogios, agradecimentos e celebrações de conquistas e valores corporativos"
      />
      <Card>
        <h2 className="text-xl font-bold text-white mb-2">Mural de Reconhecimentos</h2>
        <p className="text-slate-400 text-sm mb-6">Celebre as contribuições e atitudes dos membros do seu time.</p>
        
        <EmptyState
          title="Mural sem publicações"
          message="Nenhum elogio ou reconhecimento foi publicado recentemente."
        />
      </Card>
    </div>
  );
}
