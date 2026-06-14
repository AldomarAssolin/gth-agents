import { useState, useMemo } from "react";
import ReconhecimentoCard from "./ReconhecimentoCard";
import EmptyState from "../../components/ui/EmptyState";
import Select from "../../components/ui/Select";

export default function ReconhecimentosList({
  reconhecimentos = [],
  colaboradores = [],
  currentUser,
  onCancelar,
  showColaboradorFilter = true,
}) {
  const [filterColaborador, setFilterColaborador] = useState("");
  const [filterTipo, setFilterTipo] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  const colaboradorMap = useMemo(() => {
    const map = {};
    colaboradores.forEach((colab) => {
      map[colab.id] = colab.nome;
    });
    return map;
  }, [colaboradores]);

  const tipoOptions = [
    { label: "Todos os Tipos", value: "" },
    { label: "Destaque", value: "DESTAQUE" },
    { label: "Meta Atingida", value: "META_ATINGIDA" },
    { label: "Evolução Técnica", value: "EVOLUCAO_TECNICA" },
    { label: "Comportamento Positivo", value: "COMPORTAMENTO_POSITIVO" },
    { label: "Conclusão de Treinamento", value: "CONCLUSAO_TREINAMENTO" },
    { label: "Conclusão de PDI", value: "CONCLUSAO_PDI" },
    { label: "Redução de Retrabalho", value: "REDUCAO_RETRABALHO" },
    { label: "Apoio da Equipe", value: "APOIO_EQUIPE" },
    { label: "Potencial de Liderança", value: "POTENCIAL_LIDERANCA" },
    { label: "Outro", value: "OUTRO" },
  ];

  const statusOptions = [
    { label: "Todos os Status", value: "" },
    { label: "Ativos", value: "ativo" },
    { label: "Cancelados", value: "cancelado" },
  ];

  const filteredReconhecimentos = useMemo(() => {
    return reconhecimentos.filter((rec) => {
      const matchColaborador =
        !filterColaborador || String(rec.colaborador_id) === filterColaborador;
      const matchTipo = !filterTipo || rec.tipo === filterTipo;
      const matchStatus =
        !filterStatus ||
        (filterStatus === "ativo" && rec.ativo) ||
        (filterStatus === "cancelado" && !rec.ativo);

      return matchColaborador && matchTipo && matchStatus;
    });
  }, [reconhecimentos, filterColaborador, filterTipo, filterStatus]);

  if (reconhecimentos.length === 0) {
    return (
      <EmptyState
        title="Sem reconhecimentos"
        message="Não há reconhecimentos registrados no momento."
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Filters Card */}
      <div className="bg-slate-800 border border-slate-700/60 rounded-xl p-4 shadow-md">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {showColaboradorFilter && (
            <Select
              id="filtro-colaborador"
              label="Filtrar por Colaborador"
              value={filterColaborador}
              onChange={(e) => setFilterColaborador(e.target.value)}
              options={[
                { label: "Todos os Colaboradores", value: "" },
                ...colaboradores.map((c) => ({
                  label: c.nome,
                  value: String(c.id),
                })),
              ]}
            />
          )}
          <Select
            id="filtro-tipo"
            label="Filtrar por Tipo"
            value={filterTipo}
            onChange={(e) => setFilterTipo(e.target.value)}
            options={tipoOptions}
          />
          <Select
            id="filtro-status"
            label="Filtrar por Status"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            options={statusOptions}
          />
        </div>
      </div>

      {/* Filtered Results */}
      {filteredReconhecimentos.length === 0 ? (
        <EmptyState
          title="Filtro sem correspondência"
          message="Nenhum reconhecimento foi encontrado para as opções de filtros selecionadas."
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredReconhecimentos.map((rec) => (
            <ReconhecimentoCard
              key={rec.id}
              reconhecimento={rec}
              currentUser={currentUser}
              colaboradorNome={colaboradorMap[rec.colaborador_id]}
              onCancelar={onCancelar}
            />
          ))}
        </div>
      )}
    </div>
  );
}
