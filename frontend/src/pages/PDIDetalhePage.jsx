import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../features/auth/useAuth";
import {
  buscarPDI,
  concluirPDI,
  cancelarPDI,
  criarAcaoPDI,
  atualizarAcaoPDI,
  concluirAcaoPDI,
  cancelarAcaoPDI,
} from "../features/pdis/pdisService";
import { buscarColaboradorPorId } from "../features/colaboradores/colaboradoresService";
import { getPDIErrorMessage } from "../features/pdis/pdisErrors";
import {
  formatarData,
  traduzirOrigemPDI,
  traduzirTipoAcaoPDI,
} from "../features/pdis/pdisFormatters";
import StatusPDIBadge from "../features/pdis/StatusPDIBadge";
import StatusAcaoPDIBadge from "../features/pdis/StatusAcaoPDIBadge";
import Loading from "../components/ui/Loading";
import ErrorMessage from "../components/ui/ErrorMessage";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import Select from "../components/ui/Select";

export default function PDIDetalhePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const isGestor = ["ADMIN", "RH", "LIDER"].includes(user?.perfil);
  const pdiId = Number(id);
  const isIdValido = Number.isInteger(pdiId) && pdiId > 0;

  const [pdi, setPdi] = useState(null);
  const [colaborador, setColaborador] = useState(null);
  const [loading, setLoading] = useState(isIdValido);
  const [error, setError] = useState(isIdValido ? "" : "Identificador de PDI inválido.");
  
  // Action Modals State
  const [showAcaoModal, setShowAcaoModal] = useState(false);
  const [editingAcao, setEditingAcao] = useState(null); // If not null, we are editing
  const [acaoForm, setAcaoForm] = useState({ tipo: "TREINAMENTO", descricao: "", prazo: "" });
  const [acaoFormError, setAcaoFormError] = useState("");
  const [isAcaoSubmitting, setIsAcaoSubmitting] = useState(false);

  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Load PDI details
  useEffect(() => {
    if (!isIdValido) return;

    const controller = new AbortController();

    const carregarPDI = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await buscarPDI(pdiId, { signal: controller.signal });
        setPdi(data);

        // Fetch collaborator name
        try {
          const colData = await buscarColaboradorPorId(data.colaborador_id, {
            signal: controller.signal,
          });
          setColaborador(colData);
        } catch {
          // Keep collaborator null, fallback to ID
        }
      } catch (err) {
        if (err.name !== "CanceledError" && err.code !== "ERR_CANCELED") {
          setError(getPDIErrorMessage(err));
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    carregarPDI();

    return () => {
      controller.abort();
    };
  }, [pdiId, isIdValido, refreshTrigger]);

  const handleRefresh = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  // State Transitions
  const handleConcluirPDI = async () => {
    if (!window.confirm("Deseja realmente concluir este PDI?")) return;
    try {
      setError("");
      await concluirPDI(pdiId);
      handleRefresh(); // Screen synchronization
    } catch (err) {
      setError(getPDIErrorMessage(err));
    }
  };

  const handleCancelarPDI = async () => {
    if (!window.confirm("Deseja realmente cancelar este PDI?")) return;
    try {
      setError("");
      await cancelarPDI(pdiId);
      handleRefresh(); // Screen synchronization
    } catch (err) {
      setError(getPDIErrorMessage(err));
    }
  };

  // Action actions
  const handleConcluirAcao = async (acaoId) => {
    try {
      setError("");
      await concluirAcaoPDI(pdiId, acaoId);
      handleRefresh(); // Screen synchronization
    } catch (err) {
      setError(getPDIErrorMessage(err));
    }
  };

  const handleCancelarAcao = async (acaoId) => {
    if (!window.confirm("Deseja realmente cancelar esta ação?")) return;
    try {
      setError("");
      await cancelarAcaoPDI(pdiId, acaoId);
      handleRefresh(); // Screen synchronization
    } catch (err) {
      setError(getPDIErrorMessage(err));
    }
  };

  // Action Modals logic
  const handleOpenAddAcao = () => {
    setEditingAcao(null);
    setAcaoForm({ tipo: "TREINAMENTO", descricao: "", prazo: "" });
    setAcaoFormError("");
    setShowAcaoModal(true);
  };

  const handleOpenEditAcao = (acao) => {
    setEditingAcao(acao);
    setAcaoForm({
      tipo: acao.tipo,
      descricao: acao.descricao,
      prazo: String(acao.prazo).slice(0, 10),
    });
    setAcaoFormError("");
    setShowAcaoModal(true);
  };

  const handleAcaoSubmit = async (e) => {
    e.preventDefault();
    if (!acaoForm.descricao.trim()) {
      setAcaoFormError("Informe a descrição da ação.");
      return;
    }
    if (!acaoForm.prazo) {
      setAcaoFormError("Informe o prazo da ação.");
      return;
    }

    try {
      setIsAcaoSubmitting(true);
      setAcaoFormError("");

      const payload = {
        tipo: acaoForm.tipo,
        descricao: acaoForm.descricao.trim(),
        prazo: acaoForm.prazo,
      };

      if (editingAcao) {
        await atualizarAcaoPDI(pdiId, editingAcao.id, payload);
      } else {
        await criarAcaoPDI(pdiId, payload);
      }

      setShowAcaoModal(false);
      handleRefresh(); // Screen synchronization
    } catch (err) {
      setAcaoFormError(getPDIErrorMessage(err));
    } finally {
      setIsAcaoSubmitting(false);
    }
  };

  if (!isIdValido) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4">
        <ErrorMessage title="Erro de Validação" message={error} />
        <div className="mt-4">
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar para PDIs
          </Button>
        </div>
      </div>
    );
  }

  if (loading && !pdi) {
    return <Loading message="Carregando detalhes do PDI..." />;
  }

  if (error && !pdi) {
    return (
      <div className="max-w-4xl mx-auto py-8 px-4 space-y-4">
        <ErrorMessage title="Erro ao carregar PDI" message={error} />
        <div>
          <Button onClick={() => navigate("/pdis")} variant="secondary">
            Voltar para lista
          </Button>
        </div>
      </div>
    );
  }

  const isPdiAtivo = pdi?.status === "ATIVO" || pdi?.status === "RASCUNHO";
  const acoesList = pdi?.acoes || [];
  const totalAcoes = acoesList.length;
  const acoesConcluidas = acoesList.filter((a) => a.status === "CONCLUIDA").length;
  const acoesCanceladas = acoesList.filter((a) => a.status === "CANCELADA").length;
  const acoesPendentesCount = totalAcoes - acoesConcluidas - acoesCanceladas;

  const colaboradorNome = colaborador
    ? `${colaborador.nome} (${colaborador.matricula || colaborador.id})`
    : `Carregando... (ID: ${pdi?.colaborador_id})`;

  const tipoAcaoOptions = [
    { label: "Treinamento", value: "TREINAMENTO" },
    { label: "Mentoria", value: "MENTORIA" },
    { label: "Leitura", value: "LEITURA" },
    { label: "Prática Supervisionada", value: "PRATICA_SUPERVISIONADA" },
    { label: "Participação em Projeto", value: "PARTICIPACAO_PROJETO" },
    { label: "Acompanhamento do Líder", value: "ACOMPANHAMENTO_LIDER" },
    { label: "Outro", value: "OUTRO" },
  ];

  return (
    <div className="space-y-6">
      {/* Top Navigation Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-700">
        <div>
          <Link to="/pdis" className="text-sm text-indigo-400 hover:text-indigo-300 font-medium">
            &larr; Voltar para a lista de PDIs
          </Link>
          <h1 className="text-2xl font-bold text-white mt-1">Detalhes do PDI</h1>
        </div>

        {isGestor && isPdiAtivo && (
          <div className="flex flex-wrap gap-2 shrink-0">
            <Link to={`/pdis/${pdiId}/editar`}>
              <Button variant="outline">Editar PDI</Button>
            </Link>
            
            <Button
              onClick={handleConcluirPDI}
              variant="primary"
              disabled={acoesPendentesCount > 0}
              title={acoesPendentesCount > 0 ? "Conclua ou cancele todas as ações antes de concluir o PDI" : ""}
            >
              Concluir PDI
            </Button>
            
            <Button onClick={handleCancelarPDI} variant="secondary">
              Cancelar PDI
            </Button>
          </div>
        )}
      </div>

      {error && <ErrorMessage title="Erro na Operação" message={error} />}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side: General Info Card */}
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <div className="space-y-4">
              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Colaborador
                </span>
                <span className="text-white font-medium text-md">{colaboradorNome}</span>
              </div>

              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Status do Plano
                </span>
                <div className="mt-1">
                  <StatusPDIBadge status={pdi?.status} />
                </div>
              </div>

              <div>
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Origem do PDI
                </span>
                <span className="text-slate-300 text-sm mt-1 block">
                  {traduzirOrigemPDI(pdi?.origem)}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Data de Início
                  </span>
                  <span className="text-slate-300 text-sm">
                    {formatarData(pdi?.data_inicio)}
                  </span>
                </div>
                <div>
                  <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Data de Fim
                  </span>
                  <span className="text-slate-300 text-sm">
                    {formatarData(pdi?.data_fim)}
                  </span>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-700">
                <span className="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Progresso das Ações
                </span>
                <div className="flex items-center space-x-3 mt-2">
                  <div className="w-full bg-slate-700 rounded-full h-2.5">
                    <div
                      className="bg-indigo-500 h-2.5 rounded-full transition-all duration-300"
                      style={{
                        width: `${totalAcoes > 0 ? ((acoesConcluidas + acoesCanceladas) / totalAcoes) * 100 : 0}%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-xs text-slate-300 font-semibold whitespace-nowrap">
                    {acoesConcluidas + acoesCanceladas}/{totalAcoes} resolvidas
                  </span>
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Side: Description and Actions List */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <h2 className="text-lg font-bold text-white mb-2">Objetivos Gerais</h2>
            <h3 className="text-xl font-semibold text-indigo-300 mb-2">{pdi?.titulo}</h3>
            <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-line bg-slate-900/40 p-4 rounded-lg border border-slate-700/40">
              {pdi?.descricao}
            </p>
          </Card>

          <Card>
            <div className="flex items-center justify-between pb-4 border-b border-slate-700 mb-4">
              <div>
                <h2 className="text-lg font-bold text-white">Plano de Ações</h2>
                <p className="text-xs text-slate-400 mt-0.5">Etapas a serem cumpridas para atingir os objetivos.</p>
              </div>
              {isGestor && isPdiAtivo && (
                <Button onClick={handleOpenAddAcao} variant="outline" size="sm">
                  + Adicionar Ação
                </Button>
              )}
            </div>

            {acoesList.length === 0 ? (
              <div className="text-center py-8 text-slate-400 text-sm">
                Nenhuma ação cadastrada para este PDI.
              </div>
            ) : (
              <div className="space-y-4">
                {acoesList.map((acao) => {
                  const isAcaoAtiva = acao.status === "PENDENTE" || acao.status === "EM_ANDAMENTO";

                  return (
                    <div
                      key={acao.id}
                      className="p-4 bg-slate-800/40 border border-slate-700/50 rounded-lg hover:border-slate-600/70 transition-all flex flex-col md:flex-row md:items-start justify-between gap-4"
                    >
                      <div className="space-y-2 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-700 text-slate-300">
                            {traduzirTipoAcaoPDI(acao.tipo)}
                          </span>
                          <StatusAcaoPDIBadge status={acao.status} />
                          <span className="text-xs text-slate-400">
                            Prazo: <strong className="text-slate-300">{formatarData(acao.prazo)}</strong>
                          </span>
                        </div>
                        <p className="text-white text-sm font-medium">{acao.descricao}</p>
                      </div>

                      {isGestor && isPdiAtivo && isAcaoAtiva && (
                        <div className="flex flex-wrap gap-2 shrink-0 md:self-center">
                          <button
                            onClick={() => handleConcluirAcao(acao.id)}
                            className="px-2 py-1 text-xs font-semibold rounded bg-emerald-600/20 text-emerald-400 border border-emerald-600/40 hover:bg-emerald-600/30 cursor-pointer"
                          >
                            Concluir
                          </button>
                          <button
                            onClick={() => handleOpenEditAcao(acao)}
                            className="px-2 py-1 text-xs font-semibold rounded bg-indigo-600/20 text-indigo-400 border border-indigo-600/40 hover:bg-indigo-600/30 cursor-pointer"
                          >
                            Editar
                          </button>
                          <button
                            onClick={() => handleCancelarAcao(acao.id)}
                            className="px-2 py-1 text-xs font-semibold rounded bg-red-600/20 text-red-400 border border-red-600/40 hover:bg-red-600/30 cursor-pointer"
                          >
                            Cancelar
                          </button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </Card>
        </div>
      </div>

      {/* Action Add/Edit Modal */}
      {showAcaoModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-800 border border-slate-700 rounded-xl shadow-2xl max-w-md w-full p-6 space-y-4">
            <div>
              <h3 className="text-lg font-bold text-white">
                {editingAcao ? "Editar Ação" : "Adicionar Nova Ação"}
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Defina os parâmetros da ação de desenvolvimento.
              </p>
            </div>

            {acaoFormError && <ErrorMessage title="Erro de Validação" message={acaoFormError} />}

            <form onSubmit={handleAcaoSubmit} className="space-y-4">
              <Select
                id="modal_acao_tipo"
                label="Tipo de Ação"
                value={acaoForm.tipo}
                options={tipoAcaoOptions}
                onChange={(e) => setAForm("tipo", e.target.value)}
              />

              <Input
                id="modal_acao_prazo"
                type="date"
                label="Prazo de Conclusão"
                value={acaoForm.prazo}
                onChange={(e) => setAForm("prazo", e.target.value)}
                required
              />

              <div className="space-y-1">
                <label htmlFor="modal_acao_descricao" className="block text-sm font-medium text-slate-300">
                  Descrição da Ação
                </label>
                <textarea
                  id="modal_acao_descricao"
                  rows={3}
                  value={acaoForm.descricao}
                  onChange={(e) => setAForm("descricao", e.target.value)}
                  placeholder="Ex: Obter a certificação Professional Scrum Master I"
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                  required
                />
              </div>

              <div className="flex items-center justify-end space-x-2 pt-2">
                <Button
                  type="button"
                  onClick={() => setShowAcaoModal(false)}
                  variant="secondary"
                  disabled={isAcaoSubmitting}
                >
                  Cancelar
                </Button>
                <Button type="submit" variant="primary" disabled={isAcaoSubmitting}>
                  {isAcaoSubmitting ? "Salvando..." : "Salvar Ação"}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );

  function setAForm(field, value) {
    setAcaoForm((prev) => ({ ...prev, [field]: value }));
  }
}
