import { useState, useEffect } from "react";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

import { getDashboardMVP } from "../features/dashboard/dashboardService";
import ResumoGeral from "../features/dashboard/ResumoGeral";
import DistribuicaoPerfis from "../features/dashboard/DistribuicaoPerfis";
import AlertasDashboard from "../features/dashboard/AlertasDashboard";
import UltimasAvaliacoes from "../features/dashboard/UltimasAvaliacoes";
import UltimosFeedbacks from "../features/dashboard/UltimosFeedbacks";
import UltimosReconhecimentos from "../features/dashboard/UltimosReconhecimentos";

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [status403, setStatus403] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);

  const fetchDashboard = async () => {
    setLoading(true);
    setError(null);
    setStatus403(false);
    try {
      const data = await getDashboardMVP();
      setDashboardData(data);
    } catch (err) {
      if (err.response && err.response.status === 403) {
        setStatus403(true);
      } else if (err.response) {
        setError(
          err.response.data?.message ||
            "Não foi possível carregar as informações do dashboard."
        );
      } else if (err.request) {
        setError(
          "Não foi possível conectar à API. Verifique se o servidor está em execução."
        );
      } else {
        setError("Erro inesperado ao carregar o dashboard.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let isMounted = true;

    getDashboardMVP()
      .then((data) => {
        if (isMounted) {
          setDashboardData(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          if (err.response && err.response.status === 403) {
            setStatus403(true);
          } else if (err.response) {
            setError(
              err.response.data?.message ||
                "Não foi possível carregar as informações do dashboard."
            );
          } else if (err.request) {
            setError(
              "Não foi possível conectar à API. Verifique se o servidor está em execução."
            );
          } else {
            setError("Erro inesperado ao carregar o dashboard.");
          }
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Dashboard"
          description="Visão geral do sistema de gerenciamento de talentos e agentes de IA"
        />
        <Loading message="Carregando dados do dashboard..." />
      </div>
    );
  }

  if (status403) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Dashboard"
          description="Visão geral do sistema de gerenciamento de talentos e agentes de IA"
        />
        <ErrorMessage
          title="Acesso Negado"
          message="Você não possui permissão para acessar o dashboard geral."
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Dashboard"
          description="Visão geral do sistema de gerenciamento de talentos e agentes de IA"
        />
        <div className="space-y-4">
          <ErrorMessage title="Erro de Carregamento" message={error} />
          <div>
            <Button onClick={fetchDashboard} variant="primary">
              Tentar novamente
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <PageHeader
        title="Dashboard"
        description="Visão geral do sistema de gerenciamento de talentos e agentes de IA"
      />

      {/* 1. Resumo Geral de Métricas e Detalhes de Metas/PDIs */}
      <ResumoGeral data={dashboardData} />

      {/* 2. Distribuição e Alertas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DistribuicaoPerfis data={dashboardData} />
        <AlertasDashboard data={dashboardData} />
      </div>

      {/* 3. Últimos Registros */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <UltimasAvaliacoes data={dashboardData} />
        <UltimosFeedbacks data={dashboardData} />
        <UltimosReconhecimentos data={dashboardData} />
      </div>
    </div>
  );
}
