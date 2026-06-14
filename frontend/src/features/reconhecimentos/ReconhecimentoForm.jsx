import { useState } from "react";
import Button from "../../components/ui/Button";
import Select from "../../components/ui/Select";

export default function ReconhecimentoForm({
  colaboradores = [],
  initialColaboradorId = "",
  lockColaborador = false,
  onSubmit,
  onCancel,
  isSubmitting = false,
}) {
  const [colaboradorId, setColaboradorId] = useState(initialColaboradorId);
  const [tipo, setTipo] = useState("DESTAQUE");
  const [descricao, setDescricao] = useState("");
  const [evidencia, setEvidencia] = useState("");
  const [validationError, setValidationError] = useState("");


  const tipoOptions = [
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

  const handleSubmit = (e) => {
    e.preventDefault();
    setValidationError("");

    if (!colaboradorId) {
      setValidationError("Selecione um colaborador.");
      return;
    }
    if (!tipo) {
      setValidationError("Selecione o tipo de reconhecimento.");
      return;
    }
    if (!descricao.trim()) {
      setValidationError("A descrição do reconhecimento é obrigatória.");
      return;
    }
    if (!evidencia.trim()) {
      setValidationError("A evidência do reconhecimento é obrigatória.");
      return;
    }

    onSubmit({
      colaborador_id: Number(colaboradorId),
      tipo,
      descricao: descricao.trim(),
      evidencia: evidencia.trim(),
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

      <div>
        <Select
          id="tipo"
          name="tipo"
          label="Tipo de Reconhecimento"
          value={tipo}
          disabled={isSubmitting}
          options={tipoOptions}
          onChange={(e) => setTipo(e.target.value)}
          required
        />
      </div>

      <div className="space-y-1">
        <label htmlFor="descricao" className="block text-sm font-medium text-slate-300">
          Descrição do Reconhecimento
        </label>
        <textarea
          id="descricao"
          name="descricao"
          rows={3}
          value={descricao}
          onChange={(e) => setDescricao(e.target.value)}
          placeholder="Descreva o que motivou este reconhecimento..."
          className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
          disabled={isSubmitting}
          required
        />
      </div>

      <div className="space-y-1">
        <label htmlFor="evidencia" className="block text-sm font-medium text-slate-300">
          Evidência
        </label>
        <textarea
          id="evidencia"
          name="evidencia"
          rows={3}
          value={evidencia}
          onChange={(e) => setEvidencia(e.target.value)}
          placeholder="Cite links, documentos ou fatos observáveis que comprovem..."
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
          {isSubmitting ? "Salvando..." : "Salvar Reconhecimento"}
        </Button>
      </div>
    </form>
  );
}
