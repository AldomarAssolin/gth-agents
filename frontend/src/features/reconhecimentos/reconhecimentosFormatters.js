export function formatarData(dataString) {
  if (!dataString) return "";
  try {
    const date = new Date(dataString);
    if (isNaN(date.getTime())) return dataString;
    return date.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  } catch {
    return dataString;
  }
}

export function traduzirTipoReconhecimento(tipo) {
  const tipos = {
    DESTAQUE: "Destaque",
    META_ATINGIDA: "Meta Atingida",
    EVOLUCAO_TECNICA: "Evolução Técnica",
    COMPORTAMENTO_POSITIVO: "Comportamento Positivo",
    CONCLUSAO_TREINAMENTO: "Conclusão de Treinamento",
    CONCLUSAO_PDI: "Conclusão de PDI",
    REDUCAO_RETRABALHO: "Redução de Retrabalho",
    APOIO_EQUIPE: "Apoio da Equipe",
    POTENCIAL_LIDERANCA: "Potencial de Liderança",
    OUTRO: "Outro",
  };
  return tipos[tipo] || tipo;
}
