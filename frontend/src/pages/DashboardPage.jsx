import Layout from "../layouts/Layout";

export default function DashboardPage() {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">Dashboard</h1>
            <p className="text-slate-400 mt-1">Visão geral do sistema e agentes</p>
          </div>
        </div>

        {/* Dashboard Placeholder Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-md">
            <h3 className="text-sm font-medium text-slate-400">Total de Colaboradores</h3>
            <p className="text-3xl font-semibold text-white mt-2">12</p>
          </div>
          <div className="p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-md">
            <h3 className="text-sm font-medium text-slate-400">Agentes Ativos</h3>
            <p className="text-3xl font-semibold text-indigo-400 mt-2">4</p>
          </div>
          <div className="p-6 bg-slate-800 rounded-xl border border-slate-700 shadow-md">
            <h3 className="text-sm font-medium text-slate-400">Avaliações Pendentes</h3>
            <p className="text-3xl font-semibold text-emerald-400 mt-2">3</p>
          </div>
        </div>

        {/* Info Box */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-md">
          <h2 className="text-xl font-semibold text-white mb-4">Bem-vindo ao GTH Agents</h2>
          <p className="text-slate-300 leading-relaxed">
            Esta é a base do sistema frontend, configurada com React, Vite, Tailwind CSS e Docker.
            Utilize o menu de navegação acima para acessar a lista de colaboradores e testar o roteador.
          </p>
        </div>
      </div>
    </Layout>
  );
}
