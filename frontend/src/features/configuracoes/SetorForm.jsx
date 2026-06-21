import { useState } from "react";
import Input from "../../components/ui/Input";
import Button from "../../components/ui/Button";
import ErrorMessage from "../../components/ui/ErrorMessage";
import { getConfiguracoesErrorMessage } from "./configuracoesErrors";

export default function SetorForm({ onSubmit, onCancel, initialData }) {
  const [formData, setFormData] = useState(() => ({
    nome: initialData?.nome || "",
    descricao: initialData?.descricao || "",
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
      newErrors.nome = "Nome do setor é obrigatório.";
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
        descricao: formData.descricao.trim() || null,
      });
      if (!initialData) {
        setFormData({ nome: "", descricao: "" });
      }
    } catch (err) {
      setSubmitError(getConfiguracoesErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {submitError && (
        <ErrorMessage title="Erro ao salvar setor" message={submitError} />
      )}

      <Input
        id="setor-nome"
        name="nome"
        label="Nome do Setor"
        placeholder="Ex: Recursos Humanos, Engenharia"
        value={formData.nome}
        onChange={handleChange}
        error={errors.nome}
        disabled={submitting}
        required
      />

      <Input
        id="setor-descricao"
        name="descricao"
        label="Descrição"
        placeholder="Descrição breve do setor"
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
          {submitting ? "Salvando..." : initialData ? "Atualizar Setor" : "Salvar Setor"}
        </Button>
      </div>
    </form>
  );
}
