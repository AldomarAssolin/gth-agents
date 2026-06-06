import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Visão geral do sistema de gerenciamento de talentos e agentes de IA"
      />

      {/* Dashboard Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-medium text-slate-400">Total de Colaboradores</h3>
            <p className="text-3xl font-bold text-white mt-2">12</p>
          </div>
          <p className="text-xs text-slate-500 mt-4">2 adicionados este mês</p>
        </Card>
        
        <Card className="flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-medium text-slate-400">Agentes Ativos</h3>
            <p className="text-3xl font-bold text-indigo-400 mt-2">4</p>
          </div>
          <p className="text-xs text-indigo-500/80 mt-4">Todos operando normalmente</p>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-medium text-slate-400">Avaliações Pendentes</h3>
            <p className="text-3xl font-bold text-emerald-400 mt-2">3</p>
          </div>
          <p className="text-xs text-emerald-500/80 mt-4">Prazo termina em 5 dias</p>
        </Card>
      </div>

      {/* Welcome / Info Block */}
      <Card>
        <h2 className="text-xl font-bold text-white mb-4">GTH Agents - Base Visual</h2>
        <p className="text-slate-300 leading-relaxed">
          Esta é a nova estrutura visual da aplicação. Utilizamos uma navegação lateral integrada 
          com layouts dinâmicos e componentes UI reutilizáveis sob a stack do Tailwind CSS. 
          Use o menu de navegação à esquerda para explorar as demais rotas configuradas.
        </p>
      </Card>
    </div>
  );
}
