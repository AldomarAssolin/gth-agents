export function formatarDataBrasil(value) {
  if (!value) {
    return "Não informado";
  }

  // Handle datetime strings (ISO format)
  const datePart = String(value).slice(0, 10);
  const parts = datePart.split("-");

  if (parts.length !== 3) {
    return "Não informado";
  }

  const [year, month, day] = parts;
  if (!year || !month || !day) {
    return "Não informado";
  }

  return `${day}/${month}/${year}`;
}

export function formatarMedia(valor, totalAvaliacoes) {
  if (valor === null || valor === undefined || totalAvaliacoes === 0) {
    return "Ainda não avaliado";
  }

  const num = Number(valor);
  if (isNaN(num)) {
    return "Ainda não avaliado";
  }

  // Format with a comma as decimal separator, showing exactly one decimal place
  return num.toLocaleString("pt-BR", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  });
}

export function traduzirClassificacao(classificacao) {
  const mapa = {
    ALTA_PERFORMANCE: "Alta Performance",
    POTENCIAL_LIDER: "Potencial Líder",
    ESPECIALISTA_TECNICO: "Especialista Técnico",
    TALENTO_EM_DESENVOLVIMENTO: "Talento em Desenvolvimento",
    NECESSITA_DESENVOLVIMENTO: "Necessita Desenvolvimento",
    SEM_PERFIL: "Sem Perfil"
  };

  return mapa[classificacao] || classificacao || "Sem Perfil";
}

export function traduzirOrigemPDI(origem) {
  const mapa = {
    AVALIACAO: "Avaliação",
    MANUAL: "Manual",
    AGENTE_IA: "Agente IA",
    AVALIACAO_IA: "Avaliação IA"
  };

  return mapa[origem] || origem || "Não informada";
}

export function traduzirStatus(status) {
  const mapa = {
    ATIVO: "Ativo",
    CONCLUIDA: "Concluído",
    CONCLUIDO: "Concluído",
    ATRASADA: "Atrasado",
    ATRASADO: "Atrasado",
    PENDENTE: "Pendente",
    RASCUNHO: "Rascunho",
    CANCELADA: "Cancelado",
    CANCELADO: "Cancelado"
  };

  return mapa[status] || status || "Não informado";
}

export function traduzirPrioridade(prioridade) {
  const mapa = {
    BAIXA: "Baixa",
    MEDIA: "Média",
    ALTA: "Alta",
    CRITICA: "Crítica"
  };

  return mapa[prioridade] || prioridade || "Não informada";
}

export function traduzirNivel(nivel) {
  const mapa = {
    ALTO: "Alto",
    MEDIO: "Médio",
    BAIXO: "Baixo"
  };

  return mapa[nivel] || nivel || "Não avaliado";
}

export function traduzirTipoAvaliacao(tipo) {
  const mapa = {
    AVALIACAO_LIDER: "Avaliação do Líder",
    AUTO_AVALIACAO: "Autoavaliação",
    FEEDBACK_360: "Feedback 360°"
  };
  return mapa[tipo] || tipo || "Avaliação";
}

