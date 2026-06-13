export function traduzirStatusPDI(status) {
  const statusMap = {
    RASCUNHO: "Rascunho",
    ATIVO: "Ativo",
    CONCLUIDO: "Concluído",
    CANCELADO: "Cancelado",
  };
  return statusMap[status] || status || "Desconhecido";
}

export function traduzirOrigemPDI(origem) {
  const origemMap = {
    AVALIACAO: "Avaliação",
    FEEDBACK: "Feedback",
    META: "Meta",
    INDICACAO_LIDER: "Indicação do Líder",
    AGENTE_IA: "Agente IA",
    MANUAL: "Manual",
  };
  return origemMap[origem] || origem || "Desconhecido";
}

export function traduzirTipoAcaoPDI(tipo) {
  const tipoMap = {
    TREINAMENTO: "Treinamento",
    MENTORIA: "Mentoria",
    LEITURA: "Leitura",
    PRATICA_SUPERVISIONADA: "Prática Supervisionada",
    PARTICIPACAO_PROJETO: "Participação em Projeto",
    ACOMPANHAMENTO_LIDER: "Acompanhamento do Líder",
    OUTRO: "Outro",
  };
  return tipoMap[tipo] || tipo || "Desconhecido";
}

export function traduzirStatusAcaoPDI(status) {
  const statusMap = {
    PENDENTE: "Pendente",
    EM_ANDAMENTO: "Em andamento",
    CONCLUIDA: "Concluída",
    CANCELADA: "Cancelada",
  };
  return statusMap[status] || status || "Desconhecido";
}

export function formatarData(data) {
  if (!data) {
    return "Não informada";
  }

  const dateStr = String(data).slice(0, 10);
  const parts = dateStr.split("-");

  if (parts.length !== 3) {
    return "Data inválida";
  }

  const [ano, mes, dia] = parts;

  if (!ano || !mes || !dia || ano.length !== 4 || mes.length !== 2 || dia.length !== 2) {
    return "Data inválida";
  }

  return `${dia}/${mes}/${ano}`;
}
