import { useState } from "react";
import Button from "../../components/ui/Button";
import Select from "../../components/ui/Select";
import TipoAvaliacaoSelect from "./TipoAvaliacaoSelect";
import ItemAvaliacaoForm from "./ItemAvaliacaoForm";
import { formatTipoCompetencia } from "./avaliacaoUtils";

export default function AvaliacaoForm({
  colaboradores = [],
  competencias = [],
  onSubmit,
  onCancel,
  isSubmitting,
  initialColaboradorId = "",
  user
}) {
  const [colaboradorId, setColaboradorId] = useState(initialColaboradorId);
  const [tipo, setTipo] = useState("");
  const [observacaoGeral, setObservacaoGeral] = useState("");
  const [checkedState, setCheckedState] = useState({});
  const [notaState, setNotaState] = useState({});
  const [comentarioState, setComentarioState] = useState({});
  
  // Validation errors
  const [errors, setErrors] = useState({});

  // Group competencies
  const groupedCompetencias = {};
  competencias.forEach((comp) => {
    if (comp.ativo) {
      const category = comp.tipo || "OUTROS";
      if (!groupedCompetencias[category]) {
        groupedCompetencias[category] = [];
      }
      groupedCompetencias[category].push(comp);
    }
  });

  const handleCheckChange = (id, isChecked) => {
    setCheckedState((prev) => ({ ...prev, [id]: isChecked }));
    // Clear error for this competency when unchecked or checked
    if (errors.itens && errors.itens[id]) {
      setErrors((prev) => {
        const nextItens = { ...prev.itens };
        delete nextItens[id];
        return { ...prev, itens: nextItens };
      });
    }
  };

  const handleNotaChange = (id, val) => {
    setNotaState((prev) => ({ ...prev, [id]: val }));
    if (errors.itens && errors.itens[id]) {
      setErrors((prev) => {
        const nextItens = { ...prev.itens };
        delete nextItens[id];
        return { ...prev, itens: nextItens };
      });
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!colaboradorId) {
      newErrors.colaborador_id = "Selecione um colaborador.";
    }
    if (!tipo) {
      newErrors.tipo = "Selecione o tipo de avaliação.";
    }

    const selectedIds = Object.keys(checkedState).filter((id) => checkedState[id]);
    if (selectedIds.length === 0) {
      newErrors.competencias_geral = "Selecione pelo menos uma competência para ser avaliada.";
    } else {
      const itemErrors = {};
      selectedIds.forEach((id) => {
        const nota = notaState[id];
        if (!nota) {
          itemErrors[id] = { nota: "A nota é obrigatória." };
        } else {
          const num = Number(nota);
          if (isNaN(num) || num < 1 || num > 5 || !Number.isInteger(num)) {
            itemErrors[id] = { nota: "A nota deve ser um número inteiro de 1 a 5." };
          }
        }
      });
      if (Object.keys(itemErrors).length > 0) {
        newErrors.itens = itemErrors;
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    const selectedIds = Object.keys(checkedState).filter((id) => checkedState[id]);
    const payload = {
      colaborador_id: Number(colaboradorId),
      avaliador_id: Number(user.id),
      tipo,
      observacao_geral: observacaoGeral.trim() || null,
      itens: selectedIds.map((id) => ({
        competencia_id: Number(id),
        nota: Number(notaState[id]),
        comentario: comentarioState[id]?.trim() || null
      }))
    };

    onSubmit(payload);
  };

  const colaboradorOptions = [
    { value: "", label: "Selecione um colaborador" },
    ...colaboradores.map((c) => ({
      value: String(c.id),
      label: c.matricula ? `${c.nome} - ${c.matricula}` : c.nome
    }))
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Colaborador and Tipo Selects */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Select
          id="colaborador_id"
          label="Colaborador"
          value={colaboradorId}
          onChange={(e) => {
            setColaboradorId(e.target.value);
            if (errors.colaborador_id) {
              setErrors((prev) => ({ ...prev, colaborador_id: "" }));
            }
          }}
          options={colaboradorOptions}
          error={errors.colaborador_id}
          disabled={colaboradores.length === 0}
        />

        <TipoAvaliacaoSelect
          value={tipo}
          onChange={(e) => {
            setTipo(e.target.value);
            if (errors.tipo) {
              setErrors((prev) => ({ ...prev, tipo: "" }));
            }
          }}
          error={errors.tipo}
        />
      </div>

      {/* Observação Geral */}
      <div className="space-y-1.5">
        <label htmlFor="observacao_geral" className="block text-sm font-medium text-slate-300">
          Observação Geral
        </label>
        <textarea
          id="observacao_geral"
          rows="3"
          value={observacaoGeral}
          onChange={(e) => setObservacaoGeral(e.target.value)}
          placeholder="Comentários gerais sobre o desempenho do colaborador neste ciclo..."
          className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-sm"
        />
      </div>

      {/* Competencias Grouped */}
      <div className="space-y-6 pt-4 border-t border-slate-800">
        <div>
          <h3 className="text-lg font-bold text-white">Competências Avaliadas</h3>
          <p className="text-xs text-slate-400 mt-1">
            Selecione pelo menos uma competência abaixo e informe a nota e o comentário.
          </p>
          {errors.competencias_geral && (
            <p className="text-sm text-red-400 mt-2 font-semibold bg-red-500/10 border border-red-500/25 p-3 rounded-lg">
              {errors.competencias_geral}
            </p>
          )}
        </div>

        {Object.keys(groupedCompetencias).length === 0 ? (
          <p className="text-slate-500 text-sm italic">Nenhuma competência ativa cadastrada.</p>
        ) : (
          Object.keys(groupedCompetencias).map((category) => (
            <div key={category} className="space-y-3">
              <h4 className="text-sm font-bold text-slate-300 border-l-2 border-indigo-500 pl-2">
                {formatTipoCompetencia(category)}
              </h4>
              <div className="grid grid-cols-1 gap-4">
                {groupedCompetencias[category].map((comp) => (
                  <ItemAvaliacaoForm
                    key={comp.id}
                    competencia={comp}
                    checked={!!checkedState[comp.id]}
                    onCheckChange={(isChecked) => handleCheckChange(comp.id, isChecked)}
                    nota={notaState[comp.id] || ""}
                    onNotaChange={(val) => handleNotaChange(comp.id, val)}
                    comentario={comentarioState[comp.id] || ""}
                    onComentarioChange={(val) =>
                      setComentarioState((prev) => ({ ...prev, [comp.id]: val }))
                    }
                    error={errors.itens?.[comp.id]}
                  />
                ))}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="flex items-center justify-end space-x-3 pt-6 border-t border-slate-800">
        <Button variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancelar
        </Button>
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          {isSubmitting ? "Salvando avaliação..." : "Salvar avaliação"}
        </Button>
      </div>
    </form>
  );
}
