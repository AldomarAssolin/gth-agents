import { useState } from "react";
import Input from "../../components/ui/Input";
import Select from "../../components/ui/Select";
import Button from "../../components/ui/Button";

export default function PDIForm({
  colaboradores = [],
  initialColaboradorId = "",
  lockColaborador = false,
  initialData = null,
  isEdit = false,
  onSubmit,
  onCancel,
  isSubmitting = false,
}) {
  const [form, setForm] = useState({
    colaborador_id: initialColaboradorId || (initialData?.colaborador_id ? String(initialData.colaborador_id) : ""),
    titulo: initialData?.titulo || "",
    descricao: initialData?.descricao || "",
    data_inicio: initialData?.data_inicio ? String(initialData.data_inicio).slice(0, 10) : "",
    data_fim: initialData?.data_fim ? String(initialData.data_fim).slice(0, 10) : "",
  });

  const [acoes, setAcoes] = useState([]);
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

  // Actions list handlers (Only for creation flow)
  const handleAddAcao = () => {
    setAcoes((prev) => [
      ...prev,
      { id: Date.now(), tipo: "TREINAMENTO", descricao: "", prazo: "" },
    ]);
  };

  const handleRemoveAcao = (index) => {
    setAcoes((prev) => prev.filter((_, idx) => idx !== index));
    // Clear acoes validation error if list is modified
    if (errors.acoes) {
      setErrors((prev) => ({ ...prev, acoes: "" }));
    }
  };

  const handleAcaoChange = (index, field, value) => {
    setAcoes((prev) =>
      prev.map((acao, idx) => (idx === index ? { ...acao, [field]: value } : acao))
    );
  };

  const validate = () => {
    const newErrors = {};

    if (!isEdit && !form.colaborador_id) {
      newErrors.colaborador_id = "Selecione um colaborador.";
    }

    if (!form.titulo || !form.titulo.trim()) {
      newErrors.titulo = "Informe o título do PDI.";
    }

    if (!form.descricao || !form.descricao.trim()) {
      newErrors.descricao = "Informe a descrição do PDI.";
    }

    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;

    if (form.data_inicio && !dateRegex.test(form.data_inicio)) {
      newErrors.data_inicio = "Informe uma data inicial válida no formato AAAA-MM-DD.";
    }

    if (form.data_fim && !dateRegex.test(form.data_fim)) {
      newErrors.data_fim = "Informe uma data de término válida no formato AAAA-MM-DD.";
    }

    if (form.data_inicio && form.data_fim && form.data_inicio > form.data_fim) {
      newErrors.data_fim = "A data de término não pode ser anterior à data de início.";
    }

    // Validate actions only during creation
    if (!isEdit && acoes.length > 0) {
      const acoesErrors = [];
      acoes.forEach((acao, index) => {
        const itemError = {};
        if (!acao.descricao || !acao.descricao.trim()) {
          itemError.descricao = "Informe a descrição da ação.";
        }
        if (!acao.prazo) {
          itemError.prazo = "Informe o prazo.";
        } else if (!dateRegex.test(acao.prazo)) {
          itemError.prazo = "Prazo inválido.";
        }
        if (Object.keys(itemError).length > 0) {
          acoesErrors[index] = itemError;
        }
      });
      if (acoesErrors.length > 0) {
        newErrors.acoes = acoesErrors;
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      const payload = {
        titulo: form.titulo.trim(),
        descricao: form.descricao.trim(),
        data_inicio: form.data_inicio || null,
        data_fim: form.data_fim || null,
      };

      if (!isEdit) {
        payload.colaborador_id = Number(form.colaborador_id);
        payload.origem = "MANUAL"; // Implicit manual origin
        payload.status = "ATIVO"; // Implicit default status
        payload.acoes = acoes.map((a) => ({
          tipo: a.tipo,
          descricao: a.descricao.trim(),
          prazo: a.prazo,
        }));
      }

      onSubmit(payload);
    }
  };

  const colaboradorOptions = [
    { label: "Selecione um colaborador...", value: "" },
    ...colaboradores.map((c) => ({
      label: `${c.nome} (${c.matricula || c.id})`,
      value: String(c.id),
    })),
  ];

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
    <form onSubmit={handleSubmit} className="space-y-6">
      {!isEdit && (
        lockColaborador ? (
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
            required
          />
        )
      )}

      <Input
        id="titulo"
        name="titulo"
        label="Título do PDI"
        placeholder="Ex: Evolução Técnica e Soft Skills - Q3"
        value={form.titulo}
        onChange={handleChange}
        error={errors.titulo}
        required
      />

      <div className="space-y-1.5">
        <label htmlFor="descricao" className="block text-sm font-medium text-slate-300">
          Descrição / Objetivos do PDI
        </label>
        <textarea
          id="descricao"
          name="descricao"
          rows={4}
          placeholder="Ex: Desenvolver competências técnicas em arquitetura de microsserviços e melhorar habilidades de mentoria interna."
          className={`w-full px-4 py-2.5 bg-slate-700 border rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all ${
            errors.descricao ? "border-red-500 focus:ring-red-500" : "border-slate-600"
          }`}
          value={form.descricao}
          onChange={handleChange}
          required
        />
        {errors.descricao && <p className="text-xs text-red-400 mt-1">{errors.descricao}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input
          id="data_inicio"
          name="data_inicio"
          type="date"
          label="Data de Início (Opcional)"
          value={form.data_inicio}
          onChange={handleChange}
          error={errors.data_inicio}
        />

        <Input
          id="data_fim"
          name="data_fim"
          type="date"
          label="Data de Término (Opcional)"
          value={form.data_fim}
          onChange={handleChange}
          error={errors.data_fim}
        />
      </div>

      {/* Dynamic Actions Addition Section (Only for creation) */}
      {!isEdit && (
        <div className="pt-4 border-t border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-md font-semibold text-white">Ações de Desenvolvimento</h3>
              <p className="text-xs text-slate-400 mt-0.5">Adicione ações iniciais a serem executadas neste PDI.</p>
            </div>
            <Button type="button" onClick={handleAddAcao} variant="outline" size="sm">
              + Adicionar Ação
            </Button>
          </div>

          {acoes.length === 0 ? (
            <div className="text-center py-4 bg-slate-800/30 rounded-lg border border-dashed border-slate-700 text-slate-400 text-sm">
              Nenhuma ação inicial adicionada. É possível adicionar ações posteriormente no detalhe do PDI.
            </div>
          ) : (
            <div className="space-y-4">
              {acoes.map((acao, idx) => {
                const itemErr = errors.acoes?.[idx] || {};
                return (
                  <div key={acao.id} className="p-4 bg-slate-800/50 border border-slate-700/60 rounded-lg space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Ação #{idx + 1}</span>
                      <button
                        type="button"
                        onClick={() => handleRemoveAcao(idx)}
                        className="text-xs text-red-400 hover:text-red-300 font-semibold cursor-pointer"
                      >
                        Remover
                      </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="md:col-span-1">
                        <Select
                          id={`acao_tipo_${idx}`}
                          name="tipo"
                          label="Tipo de Ação"
                          value={acao.tipo}
                          options={tipoAcaoOptions}
                          onChange={(e) => handleAcaoChange(idx, "tipo", e.target.value)}
                        />
                      </div>
                      
                      <div className="md:col-span-1">
                        <Input
                          id={`acao_prazo_${idx}`}
                          name="prazo"
                          type="date"
                          label="Prazo"
                          value={acao.prazo}
                          onChange={(e) => handleAcaoChange(idx, "prazo", e.target.value)}
                          error={itemErr.prazo}
                          required
                        />
                      </div>

                      <div className="md:col-span-1">
                        <Input
                          id={`acao_descricao_${idx}`}
                          name="descricao"
                          label="Descrição da Ação"
                          placeholder="Ex: Concluir curso AWS Architect Associate"
                          value={acao.descricao}
                          onChange={(e) => handleAcaoChange(idx, "descricao", e.target.value)}
                          error={itemErr.descricao}
                          required
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-700">
        <Button type="button" onClick={onCancel} variant="secondary" disabled={isSubmitting}>
          Cancelar
        </Button>
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          {isSubmitting ? "Salvando..." : isEdit ? "Salvar PDI" : "Criar PDI"}
        </Button>
      </div>
    </form>
  );
}
