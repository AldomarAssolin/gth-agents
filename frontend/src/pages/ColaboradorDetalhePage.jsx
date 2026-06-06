import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";
import ColaboradorDetalhe from "../features/colaboradores/ColaboradorDetalhe";
import {
  buscarColaboradorPorId,
  listarSetores,
  listarFuncoes,
} from "../features/colaboradores/colaboradoresService";
import { getColaboradorErrorMessage } from "../features/colaboradores/colaboradoresErrors";

export default function ColaboradorDetalhePage() {
  const { id } = useParams();
  const colaboradorId = Number(id);
  const idValido = Number.isInteger(colaboradorId) && colaboradorId > 0;

  const [colaborador, setColaborador] = useState(null);
  const [setores, setSetores] = useState([]);
  const [funcoes, setFuncoes] = useState([]);
  const [loading, setLoading] = useState(idValido);
  const [error, setError] = useState(
    idValido ? "" : "Identificador de colaborador inválido."
  );
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    if (!idValido) return;

    const controller = new AbortController();

    const carregarDetalhes = async () => {
      try {
        const colabData = await buscarColaboradorPorId(colaboradorId, {
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

        setColaborador(colabData);
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

    carregarDetalhes();

    return () => {
      controller.abort();
    };
  }, [colaboradorId, idValido, retryTrigger]);

  const handleRetry = () => {
    setLoading(true);
    setError("");
    setRetryTrigger((prev) => prev + 1);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Link
          to="/colaboradores"
          className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
        >
          <span>&larr; Voltar para a lista</span>
        </Link>
      </div>

      {loading ? (
        <Loading message="Carregando detalhes do colaborador..." />
      ) : error ? (
        <div className="space-y-4">
          <ErrorMessage title="Erro ao carregar detalhes" message={error} />
          {idValido && (
            <div>
              <Button onClick={handleRetry} variant="primary">
                Tentar novamente
              </Button>
            </div>
          )}
        </div>
      ) : colaborador ? (
        <>
          <PageHeader
            title={colaborador.nome}
            description={`Matrícula: ${colaborador.matricula}`}
          />
          <ColaboradorDetalhe
            colaborador={colaborador}
            setores={setores}
            funcoes={funcoes}
          />
        </>
      ) : (
        <ErrorMessage
          title="Colaborador não encontrado"
          message="Não foi possível recuperar as informações do colaborador selecionado."
        />
      )}
    </div>
  );
}
