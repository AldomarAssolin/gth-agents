import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import { listarColaboradores } from "../features/colaboradores/colaboradoresService";
import MetasColaboradorView from "../features/metas/MetasColaboradorView";
import PageHeader from "../components/layout/PageHeader";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Button from "../components/ui/Button";
import Select from "../components/ui/Select";

export default function MetasPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const isColaboradorPerfil = user?.perfil === "COLABORADOR";
  const canCreateMeta = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);

  const [colaboradores, setColaboradores] = useState([]);
  const [loading, setLoading] = useState(!isColaboradorPerfil);
  const [error, setError] = useState("");
  const [selectedColaboradorId, setSelectedColaboradorId] = useState("");

  // Get collaborator ID from query string
  const qColaboradorId = searchParams.get("colaborador_id");

  useEffect(() => {
    if (isColaboradorPerfil) return;

    const controller = new AbortController();

    const carregarColaboradores = async () => {
      try {
        setLoading(true);
        setError("");
        const list = await listarColaboradores({ signal: controller.signal });
        setColaboradores(list);

        // Validate collaborator_id from query string
        if (qColaboradorId) {
          const parsed = Number(qColaboradorId);
          if (Number.isInteger(parsed) && parsed > 0 && list.some((c) => c.id === parsed)) {
            setSelectedColaboradorId(String(parsed));
          } else {
            // Remove invalid query param
            setSearchParams({}, { replace: true });
          }
        }
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setError("Erro ao carregar lista de colaboradores.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarColaboradores();

    return () => {
      controller.abort();
    };
  }, [isColaboradorPerfil, qColaboradorId, setSearchParams]);

  const handleColaboradorChange = (e) => {
    const value = e.target.value;
    setSelectedColaboradorId(value);
    if (value) {
      setSearchParams({ colaborador_id: value });
    } else {
      setSearchParams({});
    }
  };

  const handleCreateMeta = () => {
    if (selectedColaboradorId) {
      navigate(`/metas/nova?colaborador_id=${selectedColaboradorId}`);
    } else {
      navigate("/metas/nova");
    }
  };

  // If user is COLABORADOR
  if (isColaboradorPerfil) {
    const colId = Number(user?.colaborador_id);
    const hasColaboradorVinculo = Number.isInteger(colId) && colId > 0;

    return (
      <div className="space-y-6">
        <PageHeader
          title="Minhas Metas"
          description="Acompanhe suas metas de desempenho e OKRs para o período."
        />

        {!hasColaboradorVinculo ? (
          <ErrorMessage
            title="Vínculo Não Configurado"
            message="Seu usuário atual não possui um vínculo de colaborador configurado no sistema. Entre em contato com a administração."
          />
        ) : (
          <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-6 shadow-md">
            <MetasColaboradorView colaboradorId={colId} />
          </div>
        )}
      </div>
    );
  }

  // If user is ADMIN, RH, or LIDER
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <PageHeader
          title="Metas e OKRs"
          description="Acompanhamento e gestão de metas individuais dos colaboradores."
        />
        {canCreateMeta && (
          <div className="shrink-0">
            <Button onClick={handleCreateMeta} variant="primary">
              Criar Nova Meta
            </Button>
          </div>
        )}
      </div>

      {loading ? (
        <Loading message="Carregando colaboradores..." />
      ) : error ? (
        <ErrorMessage title="Erro de Carregamento" message={error} />
      ) : (
        <div className="space-y-6">
          <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-6 shadow-md">
            <h2 className="text-lg font-bold text-white mb-4">Consultar Metas por Colaborador</h2>

            <div className="max-w-md">
              <Select
                id="colaborador-selector"
                name="colaborador"
                label="Selecione o Colaborador"
                value={selectedColaboradorId}
                options={[
                  { label: "Selecione...", value: "" },
                  ...colaboradores.map((c) => ({
                    label: `${c.nome} (${c.matricula || c.id})`,
                    value: String(c.id),
                  })),
                ]}
                onChange={handleColaboradorChange}
              />
            </div>

            {selectedColaboradorId && (
              <div className="mt-8 pt-6 border-t border-slate-700/60">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-md font-bold text-white">
                    Lista de Metas de {colaboradores.find((c) => c.id === Number(selectedColaboradorId))?.nome}
                  </h3>
                  <Button
                    onClick={() => navigate(`/colaboradores/${selectedColaboradorId}/metas`)}
                    variant="secondary"
                    className="text-xs py-1.5 px-3"
                  >
                    Ver Página Inteira
                  </Button>
                </div>
                <MetasColaboradorView colaboradorId={selectedColaboradorId} />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
