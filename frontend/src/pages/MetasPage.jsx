import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";

export default function MetasPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Metas e OKRs"
        description="Acompanhamento de metas individuais, de equipe e organizacionais"
      />
      <Card>
        <h2 className="text-xl font-bold text-white mb-2">Objetivos Estratégicos</h2>
        <p className="text-slate-400 text-sm mb-6">Monitore os resultados chave definidos para o período corrente.</p>
        
        <EmptyState
          title="Nenhuma meta definida"
          message="Nenhum OKR ou meta individual foi vinculado ao seu usuário ou equipe para este trimestre."
        />
      </Card>
    </div>
  );
}
