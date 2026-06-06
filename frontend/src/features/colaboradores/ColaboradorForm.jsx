import { useState, useEffect } from "react";
import Input from "../../components/ui/Input";
import Select from "../../components/ui/Select";
import Button from "../../components/ui/Button";
import ErrorMessage from "../../components/ui/ErrorMessage";
import { listarSetores, listarFuncoes } from "./colaboradoresService";
import { getColaboradorErrorMessage } from "./colaboradoresErrors";

export default function ColaboradorForm({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    nome: "",
    matricula: "",
    email: "",
    data_admissao: "",
    setor_id: "",
    funcao_id: "",
  });

  const [errors, setErrors] = useState({});
  const [setores, setSetores] = useState([]);
  const [funcoes, setFuncoes] = useState([]);
  const [loadingLists, setLoadingLists] = useState(true);
  const [errorLists, setErrorLists] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    const fetchLists = async () => {
      try {
        const [setoresData, funcoesData] = await Promise.all([
          listarSetores({ signal: controller.signal }),
          listarFuncoes({ signal: controller.signal }),
        ]);
        setSetores(setoresData);
        setFuncoes(funcoesData);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setErrorLists("Não foi possível carregar os setores ou funções.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoadingLists(false);
        }
      }
    };

    fetchLists();

    return () => {
      controller.abort();
    };
  }, [retryTrigger]);

  const handleRetryLists = () => {
    setLoadingLists(true);
    setErrorLists("");
    setRetryTrigger((prev) => prev + 1);
  };

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
      newErrors.nome = "Nome completo é obrigatório.";
    }

    if (!formData.matricula.trim()) {
      newErrors.matricula = "Matrícula é obrigatória.";
    }

    if (!formData.setor_id) {
      newErrors.setor_id = "Setor é obrigatório.";
    }

    if (!formData.funcao_id) {
      newErrors.funcao_id = "Função é obrigatória.";
    }

    if (formData.email.trim()) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.email.trim())) {
        newErrors.email = "Formato de e-mail corporativo inválido.";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    setSubmitError("");

    const payload = {
      nome: formData.nome.trim(),
      matricula: formData.matricula.trim(),
      email: formData.email.trim() || null,
      data_admissao: formData.data_admissao || null,
      setor_id: Number(formData.setor_id),
      funcao_id: Number(formData.funcao_id),
    };

    try {
      await onSubmit(payload);
    } catch (err) {
      setSubmitError(getColaboradorErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const sectorOptions = [
    {
      value: "",
      label: loadingLists ? "Carregando setores..." : "Selecione um setor...",
    },
    ...setores.map((s) => ({ value: String(s.id), label: s.nome })),
  ];

  const functionOptions = [
    {
      value: "",
      label: loadingLists ? "Carregando funções..." : "Selecione uma função...",
    },
    ...funcoes.map((f) => ({ value: String(f.id), label: f.nome })),
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {submitError && (
        <ErrorMessage title="Erro ao salvar cadastro" message={submitError} />
      )}

      {errorLists && (
        <div className="space-y-3 p-4 bg-red-500/10 border border-red-500/25 rounded-xl">
          <p className="text-sm text-red-400 font-semibold">{errorLists}</p>
          <Button type="button" variant="outline" onClick={handleRetryLists} size="sm">
            Tentar novamente
          </Button>
        </div>
      )}

      <Input
        id="colab-nome"
        name="nome"
        label="Nome Completo"
        placeholder="Nome do colaborador"
        value={formData.nome}
        onChange={handleChange}
        error={errors.nome}
        disabled={submitting}
        required
      />

      <Input
        id="colab-matricula"
        name="matricula"
        label="Matrícula"
        placeholder="Código ou matrícula institucional"
        value={formData.matricula}
        onChange={handleChange}
        error={errors.matricula}
        disabled={submitting}
        required
      />

      <Input
        id="colab-email"
        name="email"
        type="email"
        label="E-mail Corporativo"
        placeholder="exemplo@empresa.com"
        value={formData.email}
        onChange={handleChange}
        error={errors.email}
        disabled={submitting}
      />

      <Input
        id="colab-data-admissao"
        name="data_admissao"
        type="date"
        label="Data de Admissão"
        value={formData.data_admissao}
        onChange={handleChange}
        disabled={submitting}
      />

      <Select
        id="colab-setor"
        name="setor_id"
        label="Setor"
        options={sectorOptions}
        value={formData.setor_id}
        onChange={handleChange}
        error={errors.setor_id}
        disabled={loadingLists || submitting || !!errorLists}
        required
      />

      <Select
        id="colab-funcao"
        name="funcao_id"
        label="Função"
        options={functionOptions}
        value={formData.funcao_id}
        onChange={handleChange}
        error={errors.funcao_id}
        disabled={loadingLists || submitting || !!errorLists}
        required
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
        <Button
          type="submit"
          variant="primary"
          disabled={loadingLists || submitting || !!errorLists}
        >
          {submitting ? "Salvando..." : "Salvar Cadastro"}
        </Button>
      </div>
    </form>
  );
}
