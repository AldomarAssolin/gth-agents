import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";
import EmptyState from "../components/ui/EmptyState";
import ColaboradoresTable from "../features/colaboradores/ColaboradoresTable";
import { useAuth } from "../features/auth/useAuth";
import {
  listarColaboradores,
  listarSetores,
  listarFuncoes,
} from "../features/colaboradores/colaboradoresService";
import { getColaboradorErrorMessage } from "../features/colaboradores/colaboradoresErrors";

export default function ColaboradoresPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [colaboradores, setColaboradores] = useState([]);
  const [setores, setSetores] = useState([]);
  const [funcoes, setFuncoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [retryTrigger, setRetryTrigger] = useState(0);

  const canCreateColaborador = ["ADMIN", "RH"].includes(user?.perfil);

  useEffect(() => {
    const controller = new AbortController();

    const carregarDados = async () => {
      try {
        const colaboradoresData = await listarColaboradores({
          signal: controller.signal,
        });

        const [setoresResult, funcoesResult] = await Promise.allSettled([
          listarSetores({ signal: controller.signal }),
          listarFuncoes({ signal: controller.signal }),
        ]);

        const setoresData =
          setoresResult.status === "fulfilled" ? setoresResult.value : [];
        const funcoesData =
          funcoesResult.status === "fulfilled" ? funcoesResult.value : [];

        setColaboradores(colaboradoresData);
        setSetores(setoresData);
        setFuncoes(funcoesData);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setError(getColaboradorErrorMessage(err));
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarDados();

    return () => {
      controller.abort();
    };
  }, [retryTrigger]);

  const handleCreateNew = () => {
    navigate("/colaboradores/novo");
  };

  const handleRetry = () => {
    setLoading(true);
    setError("");
    setRetryTrigger((prev) => prev + 1);
  };

  const headerActions = canCreateColaborador ? (
    <Button onClick={handleCreateNew} variant="primary">
      Novo Colaborador
    </Button>
  ) : null;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Colaboradores"
        description="Gerencie os membros da sua equipe e acesse seus históricos"
        actions={headerActions}
      />

      {loading ? (
        <Loading message="Carregando colaboradores..." />
      ) : error ? (
        <div className="space-y-4">
          <ErrorMessage title="Erro ao carregar colaboradores" message={error} />
          <div>
            <Button onClick={handleRetry} variant="primary">
              Tentar novamente
            </Button>
          </div>
        </div>
      ) : colaboradores.length === 0 ? (
        <div className="space-y-6 flex flex-col items-center">
          <EmptyState
            title="Nenhum colaborador encontrado"
            message={
              canCreateColaborador
                ? "Cadastre o primeiro colaborador para iniciar a gestão da equipe."
                : "Não há colaboradores cadastrados no sistema."
            }
            className="w-full"
          />
          {canCreateColaborador && (
            <Button onClick={handleCreateNew} variant="primary">
              Cadastrar Colaborador
            </Button>
          )}
        </div>
      ) : (
        <ColaboradoresTable
          colaboradores={colaboradores}
          setores={setores}
          funcoes={funcoes}
        />
      )}
    </div>
  );
}
