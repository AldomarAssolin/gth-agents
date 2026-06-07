import { useState } from "react";
import Input from "../../components/ui/Input";
import Select from "../../components/ui/Select";
import Button from "../../components/ui/Button";

export default function MetaForm({
  colaboradores = [],
  initialColaboradorId = "",
  lockColaborador = false,
  onSubmit,
  onCancel,
  isSubmitting = false,
}) {
  const [form, setForm] = useState({
    colaborador_id: initialColaboradorId || "",
    titulo: "",
    descricao: "",
    indicador: "",
    prazo: "",
    prioridade: "MEDIA",
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!form.colaborador_id) {
      newErrors.colaborador_id = "Selecione um colaborador.";
    } else {
      const colId = Number(form.colaborador_id);
      if (!Number.isInteger(colId) || colId <= 0) {
        newErrors.colaborador_id = "Colaborador inválido.";
      } else if (!colaboradores.some((c) => c.id === colId)) {
        newErrors.colaborador_id = "Colaborador não está no seu escopo ou não existe.";
      }
    }

    if (!form.titulo || !form.titulo.trim()) {
      newErrors.titulo = "Informe o título da meta.";
    }

    if (!form.descricao || !form.descricao.trim()) {
      newErrors.descricao = "Informe a descrição da meta.";
    }

    if (!form.prazo) {
      newErrors.prazo = "Informe o prazo.";
    } else {
      const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
      if (!dateRegex.test(form.prazo)) {
        newErrors.prazo = "Informe uma data válida no formato AAAA-MM-DD.";
      }
    }

    const validPrioridades = ["BAIXA", "MEDIA", "ALTA", "CRITICA"];
    if (!form.prioridade || !validPrioridades.includes(form.prioridade)) {
      newErrors.prioridade = "Selecione uma prioridade válida.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit({
        colaborador_id: Number(form.colaborador_id),
        titulo: form.titulo.trim(),
        descricao: form.descricao.trim(),
        indicador: form.indicador.trim() || null,
        prazo: form.prazo,
        prioridade: form.prioridade,
      });
    }
  };

  const colaboradorOptions = [
    { label: "Selecione um colaborador...", value: "" },
    ...colaboradores.map((c) => ({
      label: `${c.nome} (${c.matricula || c.id})`,
      value: String(c.id),
    })),
  ];

  const prioridadeOptions = [
    { label: "Baixa", value: "BAIXA" },
    { label: "Média", value: "MEDIA" },
    { label: "Alta", value: "ALTA" },
    { label: "Crítica", value: "CRITICA" },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {lockColaborador ? (
        <div className="space-y-1.5">
          <span className="block text-sm font-medium text-slate-400">Colaborador</span>
          <div className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-300">
            {colaboradores.find((c) => c.id === Number(form.colaborador_id))?.nome || `Colaborador #${form.colaborador_id}`}
          </div>
        </div>
      ) : (
        <Select
          id="colaborador_id"
          name="colaborador_id"
          label="Colaborador"
          value={form.colaborador_id}
          options={colaboradorOptions}
          onChange={handleChange}
          error={errors.colaborador_id}
        />
      )}

      <Input
        id="titulo"
        name="titulo"
        label="Título da Meta"
        placeholder="Ex: Melhorar cobertura de testes unitários"
        value={form.titulo}
        onChange={handleChange}
        error={errors.titulo}
        required
      />

      <div className="space-y-1.5">
        <label htmlFor="descricao" className="block text-sm font-medium text-slate-300">
          Descrição da Meta
        </label>
        <textarea
          id="descricao"
          name="descricao"
          rows={4}
          placeholder="Ex: Escrever testes automatizados para os controllers principais do backend."
          className={`w-full px-4 py-2.5 bg-slate-700 border rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all ${
            errors.descricao ? "border-red-500 focus:ring-red-500" : "border-slate-600"
          }`}
          value={form.descricao}
          onChange={handleChange}
          required
        />
        {errors.descricao && <p className="text-xs text-red-400 mt-1">{errors.descricao}</p>}
      </div>

      <Input
        id="indicador"
        name="indicador"
        label="Indicador / Critério de Sucesso (Opcional)"
        placeholder="Ex: Atingir 80% de cobertura nos novos arquivos"
        value={form.indicador}
        onChange={handleChange}
        error={errors.indicador}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input
          id="prazo"
          name="prazo"
          type="date"
          label="Prazo"
          value={form.prazo}
          onChange={handleChange}
          error={errors.prazo}
          required
        />

        <Select
          id="prioridade"
          name="prioridade"
          label="Prioridade"
          value={form.prioridade}
          options={prioridadeOptions}
          onChange={handleChange}
          error={errors.prioridade}
        />
      </div>

      <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-700">
        <Button onClick={onCancel} variant="secondary" disabled={isSubmitting}>
          Cancelar
        </Button>
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          {isSubmitting ? "Salvando..." : "Salvar Meta"}
        </Button>
      </div>
    </form>
  );
}
