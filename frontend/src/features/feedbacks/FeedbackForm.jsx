import { useState } from "react";
import Button from "../../components/ui/Button";
import Select from "../../components/ui/Select";

export default function FeedbackForm({
  colaboradores = [],
  initialColaboradorId = "",
  lockColaborador = false,
  onSubmit,
  onCancel,
  isSubmitting = false,
}) {
  const [colaboradorId, setColaboradorId] = useState(initialColaboradorId);
  const [contexto, setContexto] = useState("");
  const [pontoPositivo, setPontoPositivo] = useState("");
  const [pontoMelhoria, setPontoMelhoria] = useState("");
  const [acaoRecomendada, setAcaoRecomendada] = useState("");
  const [validationError, setValidationError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setValidationError("");

    if (!colaboradorId) {
      setValidationError("Selecione um colaborador.");
      return;
    }
    if (!pontoPositivo.trim()) {
      setValidationError("O ponto positivo é obrigatório.");
      return;
    }
    if (!acaoRecomendada.trim()) {
      setValidationError("A ação recomendada é obrigatória.");
      return;
    }

    onSubmit({
      colaborador_id: Number(colaboradorId),
      contexto: contexto.trim() || null,
      ponto_positivo: pontoPositivo.trim(),
      ponto_melhoria: pontoMelhoria.trim() || null,
      acao_recomendada: acaoRecomendada.trim(),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {validationError && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm px-3 py-2 rounded-lg">
          {validationError}
        </div>
      )}

      <div>
        <Select
          id="colaborador_id"
          name="colaborador_id"
          label="Colaborador"
          value={colaboradorId}
          disabled={lockColaborador || isSubmitting}
          options={[
            { label: "Selecione...", value: "" },
            ...colaboradores.map((c) => ({
              label: `${c.nome} (${c.matricula || c.id})`,
              value: String(c.id),
            })),
          ]}
          onChange={(e) => setColaboradorId(e.target.value)}
          required
        />
      </div>

      <div className="space-y-1">
        <label htmlFor="contexto" className="block text-sm font-medium text-slate-300">
          Contexto (Opcional)
        </label>
        <input
          type="text"
          id="contexto"
          name="contexto"
          value={contexto}
          onChange={(e) => setContexto(e.target.value)}
          placeholder="Ex: Reunião de alinhamento, Fechamento de sprint..."
          className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
          disabled={isSubmitting}
        />
      </div>

      <div className="space-y-1">
        <label htmlFor="ponto_positivo" className="block text-sm font-medium text-slate-300">
          Pontos Positivos
        </label>
        <textarea
          id="ponto_positivo"
          name="ponto_positivo"
          rows={3}
          value={pontoPositivo}
          onChange={(e) => setPontoPositivo(e.target.value)}
          placeholder="Descreva as fortalezas demonstradas pelo colaborador..."
          className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
          disabled={isSubmitting}
          required
        />
      </div>

      <div className="space-y-1">
        <label htmlFor="ponto_melhoria" className="block text-sm font-medium text-slate-300">
          Pontos de Melhoria (Opcional)
        </label>
        <textarea
          id="ponto_melhoria"
          name="ponto_melhoria"
          rows={3}
          value={pontoMelhoria}
          onChange={(e) => setPontoMelhoria(e.target.value)}
          placeholder="Descreva oportunidades de desenvolvimento ou comportamentos a ajustar..."
          className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
          disabled={isSubmitting}
        />
      </div>

      <div className="space-y-1">
        <label htmlFor="acao_recomendada" className="block text-sm font-medium text-slate-300">
          Ação Recomendada
        </label>
        <textarea
          id="acao_recomendada"
          name="acao_recomendada"
          rows={3}
          value={acaoRecomendada}
          onChange={(e) => setAcaoRecomendada(e.target.value)}
          placeholder="Descreva os próximos passos práticos acordados..."
          className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
          disabled={isSubmitting}
          required
        />
      </div>

      <div className="flex items-center justify-end space-x-2 pt-2">
        <Button
          type="button"
          onClick={onCancel}
          variant="secondary"
          disabled={isSubmitting}
        >
          Cancelar
        </Button>
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          {isSubmitting ? "Salvando..." : "Salvar Feedback"}
        </Button>
      </div>
    </form>
  );
}
