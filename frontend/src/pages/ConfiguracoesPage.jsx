import { Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";
import { useAuth } from "../features/auth/useAuth";

export default function ConfiguracoesPage() {
  const { user } = useAuth();
  const canAccess = ["ADMIN", "RH"].includes(user?.perfil);

  if (!canAccess) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Configurações"
          description="Gerencie as configurações e preferências do sistema"
        />
        <div className="space-y-4 max-w-2xl">
          <ErrorMessage
            title="Acesso Negado"
            message="Você não possui permissão de Administrador ou RH para acessar as configurações do sistema."
          />
          <div>
            <Link to="/">
              <Button variant="secondary">Voltar ao Início</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const cards = [
    {
      title: "Setores",
      description: "Gerencie as áreas organizacionais e a estrutura de departamentos dos colaboradores.",
      link: "/configuracoes/setores",
      iconColor: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20",
      svg: (
        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
    },
    {
      title: "Funções",
      description: "Gerencie os cargos, funções e atribuições técnicas cadastrados na organização.",
      link: "/configuracoes/funcoes",
      iconColor: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
      svg: (
        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
    },
    {
      title: "Usuários",
      description: "Gerencie os acessos, perfis (Líder, RH, Admin, Colaborador) e permissões de usuários.",
      link: "/configuracoes/usuarios",
      iconColor: "text-amber-400 bg-amber-500/10 border-amber-500/20",
      svg: (
        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      ),
    },
    {
      title: "Competências",
      description: "Gerencie as competências técnicas e comportamentais avaliadas na organização.",
      link: "/configuracoes/competencias",
      iconColor: "text-purple-400 bg-purple-500/10 border-purple-500/20",
      svg: (
        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Configurações"
        description="Painel de administração e gerenciamento de cadastros básicos do GTH Agents"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {cards.map((card, idx) => (
          <Link key={idx} to={card.link} className="block group">
            <Card className="h-full border border-slate-700 hover:border-slate-500 hover:shadow-lg transition-all duration-300 transform group-hover:-translate-y-1">
              <div className="flex items-start space-x-4">
                <div className={`p-3 rounded-xl border ${card.iconColor} shrink-0`}>
                  {card.svg}
                </div>
                <div className="space-y-1.5">
                  <h3 className="text-xl font-bold text-white group-hover:text-indigo-400 transition-colors">
                    {card.title}
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    {card.description}
                  </p>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
