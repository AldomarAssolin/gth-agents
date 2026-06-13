import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { buscarColaboradorPorId } from "../features/colaboradores/colaboradoresService";
import PDIsColaboradorView from "../features/pdis/PDIsColaboradorView";
import PageHeader from "../components/layout/PageHeader";
import Card from "../components/ui/Card";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";

export default function PDIsColaboradorPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const collaboratorId = Number(id);
  const isIdValido = Number.isInteger(collaboratorId) && collaboratorId > 0;
  
  const [colaborador, setColaborador] = useState(null);
  const [loading, setLoading] = useState(isIdValido);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isIdValido) return;

    const controller = new AbortController();

    const carregarColaborador = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await buscarColaboradorPorId(collaboratorId, {
          signal: controller.signal,
        });
        setColaborador(data);
      } catch (err) {
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED") {
          setError("Erro ao carregar dados do colaborador.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarColaborador();

    return () => {
      controller.abort();
    };
  }, [collaboratorId, isIdValido]);

  if (!isIdValido) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4">
        <ErrorMessage title="Identificador Inválido" message="O identificador do colaborador fornecido é inválido." />
        <div className="mt-4">
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Ir para PDIs
          </Button>
        </div>
      </div>
    );
  }

  if (loading && !colaborador) {
    return <Loading message="Carregando informações do colaborador..." />;
  }

  if (error && !colaborador) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4 space-y-4">
        <ErrorMessage title="Erro" message={error} />
        <div>
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar para PDIs
          </Button>
        </div>
      </div>
    );
  }

  const isOwnProfile = user?.colaborador_id === collaboratorId;
  const isGestor = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);
  const canView = isOwnProfile || isGestor;

  if (!canView) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4">
        <ErrorMessage
          title="Acesso Negado"
          message="Você não possui permissão para acessar os PDIs deste colaborador."
        />
        <div className="mt-4">
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar
          </Button>
        </div>
      </div>
    );
  }

  const colaboradorLabel = colaborador
    ? `${colaborador.nome} (${colaborador.matricula || colaborador.id})`
    : `Colaborador #${collaboratorId}`;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <Link
            to={isGestor ? `/colaboradores/${collaboratorId}` : "/pdis"}
            className="text-sm text-indigo-400 hover:text-indigo-300 font-medium"
          >
            &larr; Voltar para perfil do colaborador
          </Link>
          <PageHeader
            title={`PDIs de ${colaborador?.nome || "Colaborador"}`}
            description={`Planos de Desenvolvimento Individual associados a ${colaboradorLabel}`}
          />
        </div>

        {isGestor && (
          <div className="shrink-0">
            <Link to={`/pdis/novo?colaborador_id=${collaboratorId}`}>
              <Button variant="primary">Criar PDI para Colaborador</Button>
            </Link>
          </div>
        )}
      </div>

      <Card>
        <PDIsColaboradorView colaboradorId={collaboratorId} />
      </Card>
    </div>
  );
}
