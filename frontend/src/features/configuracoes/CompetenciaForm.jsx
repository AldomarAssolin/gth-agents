import { useState } from "react";
import Input from "../../components/ui/Input";
import Select from "../../components/ui/Select";
import Button from "../../components/ui/Button";
import ErrorMessage from "../../components/ui/ErrorMessage";
import { getConfiguracoesErrorMessage } from "./configuracoesErrors";

export default function CompetenciaForm({ onSubmit, onCancel, initialData }) {
  const [formData, setFormData] = useState(() => ({
    nome: initialData?.nome || "",
    tipo: initialData?.tipo || "TECNICA",
    descricao: initialData?.descricao || "",
    peso: initialData?.peso ? String(initialData.peso) : "1.0",
  }));

  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.nome.trim()) {
      newErrors.nome = "Nome da competência é obrigatório.";
    }

    const pesoVal = parseFloat(formData.peso);
    if (isNaN(pesoVal) || pesoVal <= 0) {
      newErrors.peso = "O peso deve ser um número maior que zero.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    setSubmitError("");

    try {
      await onSubmit({
        nome: formData.nome.trim(),
        tipo: formData.tipo,
        descricao: formData.descricao.trim() || null,
        peso: parseFloat(formData.peso),
      });
      if (!initialData) {
        setFormData({
          nome: "",
          tipo: "TECNICA",
          descricao: "",
          peso: "1.0",
        });
      }
    } catch (err) {
      setSubmitError(getConfiguracoesErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const tipoOptions = [
    { value: "TECNICA", label: "Técnica" },
    { value: "COMPORTAMENTAL", label: "Comportamental" },
    { value: "LIDERANCA", label: "Liderança" },
    { value: "ORGANIZACIONAL", label: "Organizacional" },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {submitError && (
        <ErrorMessage title="Erro ao salvar competência" message={submitError} />
      )}

      <Input
        id="comp-nome"
        name="nome"
        label="Nome da Competência"
        placeholder="Ex: Trabalho em Equipe, React, SQL"
        value={formData.nome}
        onChange={handleChange}
        error={errors.nome}
        disabled={submitting}
        required
      />

      <Select
        id="comp-tipo"
        name="tipo"
        label="Tipo de Competência"
        options={tipoOptions}
        value={formData.tipo}
        onChange={handleChange}
        disabled={submitting}
        required
      />

      <Input
        id="comp-peso"
        name="peso"
        type="number"
        step="0.01"
        label="Peso"
        placeholder="Ex: 1.0, 1.5, 2.0"
        value={formData.peso}
        onChange={handleChange}
        error={errors.peso}
        disabled={submitting}
        required
      />

      <Input
        id="comp-descricao"
        name="descricao"
        label="Descrição"
        placeholder="Descrição breve do que esta competência avalia"
        value={formData.descricao}
        onChange={handleChange}
        error={errors.descricao}
        disabled={submitting}
      />

      <div className="flex justify-end space-x-3 pt-4 border-t border-slate-700">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={submitting}
        >
          Cancelar
        </Button>
        <Button type="submit" variant="primary" disabled={submitting}>
          {submitting ? "Salvando..." : initialData ? "Atualizar Competência" : "Salvar Competência"}
        </Button>
      </div>
    </form>
  );
}
