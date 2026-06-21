import { useState, useEffect } from "react";
import Input from "../../components/ui/Input";
import Select from "../../components/ui/Select";
import Button from "../../components/ui/Button";
import ErrorMessage from "../../components/ui/ErrorMessage";
import { listarColaboradores } from "../colaboradores/colaboradoresService";
import { listarSetores } from "./setoresService";
import { getConfiguracoesErrorMessage } from "./configuracoesErrors";

export default function UsuarioForm({ onSubmit, onCancel, initialData }) {
  const [formData, setFormData] = useState(() => ({
    nome: initialData?.nome || "",
    email: initialData?.email || "",
    senha: "",
    perfil: initialData?.perfil || "COLABORADOR",
    colaborador_id: initialData?.colaborador_id ? String(initialData.colaborador_id) : "",
    setor_id: initialData?.setor_id ? String(initialData.setor_id) : "",
  }));

  const [errors, setErrors] = useState({});
  const [colaboradores, setColaboradores] = useState([]);
  const [setores, setSetores] = useState([]);
  const [loadingLists, setLoadingLists] = useState(true);
  const [errorLists, setErrorLists] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [retryTrigger, setRetryTrigger] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    const fetchLists = async () => {
      try {
        const [colaboradoresData, setoresData] = await Promise.all([
          listarColaboradores({ signal: controller.signal }),
          listarSetores({ signal: controller.signal }),
        ]);
        setColaboradores(colaboradoresData);
        setSetores(setoresData);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setErrorLists("Não foi possível carregar os colaboradores ou setores.");
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
      newErrors.nome = "Nome do usuário é obrigatório.";
    }

    if (!formData.email.trim()) {
      newErrors.email = "E-mail é obrigatório.";
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.email.trim())) {
        newErrors.email = "Formato de e-mail inválido.";
      }
    }

    if (!initialData && !formData.senha.trim()) {
      newErrors.senha = "Senha é obrigatória para novos usuários.";
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
      email: formData.email.trim(),
      perfil: formData.perfil,
      colaborador_id: formData.colaborador_id ? Number(formData.colaborador_id) : null,
      setor_id: formData.setor_id ? Number(formData.setor_id) : null,
    };

    // Only send password if it is filled
    if (formData.senha) {
      payload.senha = formData.senha;
    }

    // Security requirement: Always clear the password input field immediately
    setFormData((prev) => ({ ...prev, senha: "" }));

    try {
      await onSubmit(payload);
      if (!initialData) {
        setFormData({
          nome: "",
          email: "",
          senha: "",
          perfil: "COLABORADOR",
          colaborador_id: "",
          setor_id: "",
        });
      }
    } catch (err) {
      setSubmitError(getConfiguracoesErrorMessage(err));
      // Non-sensitive fields are preserved
    } finally {
      setSubmitting(false);
    }
  };

  const perfilOptions = [
    { value: "COLABORADOR", label: "Colaborador" },
    { value: "LIDER", label: "Líder" },
    { value: "RH", label: "RH" },
    { value: "ADMIN", label: "Administrador" },
  ];

  const colabOptions = [
    { value: "", label: "Sem colaborador associado" },
    ...colaboradores.map((c) => ({
      value: String(c.id),
      label: `${c.nome} (Matrícula: ${c.matricula})`,
    })),
  ];

  const setorOptions = [
    { value: "", label: "Sem setor associado" },
    ...setores.map((s) => ({ value: String(s.id), label: s.nome })),
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {submitError && (
        <ErrorMessage title="Erro ao salvar usuário" message={submitError} />
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
        id="user-nome"
        name="nome"
        label="Nome Completo"
        placeholder="Nome do usuário"
        value={formData.nome}
        onChange={handleChange}
        error={errors.nome}
        disabled={submitting}
        required
      />

      <Input
        id="user-email"
        name="email"
        type="email"
        label="E-mail"
        placeholder="exemplo@empresa.com"
        value={formData.email}
        onChange={handleChange}
        error={errors.email}
        disabled={submitting}
        required
      />

      <Input
        id="user-senha"
        name="senha"
        type="password"
        label={initialData ? "Senha (opcional)" : "Senha"}
        placeholder={initialData ? "Deixe em branco para manter a atual" : "Digite a senha de acesso"}
        value={formData.senha}
        onChange={handleChange}
        error={errors.senha}
        disabled={submitting}
        required={!initialData}
      />

      <Select
        id="user-perfil"
        name="perfil"
        label="Perfil de Acesso"
        options={perfilOptions}
        value={formData.perfil}
        onChange={handleChange}
        disabled={submitting}
        required
      />

      {errorLists ? (
        <>
          <Input
            id="user-colaborador-id"
            name="colaborador_id"
            type="number"
            label="ID do Colaborador (Entrada manual)"
            placeholder="Digite o ID do colaborador"
            value={formData.colaborador_id}
            onChange={handleChange}
            disabled={submitting}
          />
          <Input
            id="user-setor-id"
            name="setor_id"
            type="number"
            label="ID do Setor (Entrada manual)"
            placeholder="Digite o ID do setor"
            value={formData.setor_id}
            onChange={handleChange}
            disabled={submitting}
          />
        </>
      ) : (
        <>
          <Select
            id="user-colaborador"
            name="colaborador_id"
            label="Colaborador Associado"
            options={colabOptions}
            value={formData.colaborador_id}
            onChange={handleChange}
            disabled={loadingLists || submitting}
          />
          <Select
            id="user-setor"
            name="setor_id"
            label="Setor Associado"
            options={setorOptions}
            value={formData.setor_id}
            onChange={handleChange}
            disabled={loadingLists || submitting}
          />
        </>
      )}

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
          {submitting ? "Salvando..." : initialData ? "Atualizar Usuário" : "Salvar Usuário"}
        </Button>
      </div>
    </form>
  );
}
