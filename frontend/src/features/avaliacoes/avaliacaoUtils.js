export function formatClassificacao(classificacao) {
  if (!classificacao) return "Não informado";
  
  const map = {
    ESPECIALISTA_TECNICO: "Especialista Técnico",
    POTENCIAL_LIDER: "Potencial Líder",
    ALTA_PERFORMANCE: "Alta Performance",
    TALENTO_EM_DESENVOLVIMENTO: "Talento em Desenvolvimento",
    NECESSITA_DESENVOLVIMENTO: "Necessita Desenvolvimento"
  };
  
  return map[classificacao] ?? classificacao;
}

export function formatTipo(tipo) {
  if (!tipo) return "Não informado";
  
  const map = {
    AUTOAVALIACAO: "Autoavaliação",
    AVALIACAO_LIDER: "Avaliação do líder",
    AVALIACAO_TECNICA: "Avaliação técnica",
    AVALIACAO_360: "Avaliação 360°"
  };
  
  return map[tipo] ?? tipo;
}

export function formatTipoCompetencia(tipo) {
  if (!tipo) return "Outras";
  
  const map = {
    TECNICA: "Técnicas",
    COMPORTAMENTAL: "Comportamentais",
    LIDERANCA: "Liderança",
    ORGANIZACIONAL: "Organizacionais"
  };
  
  return map[tipo] ?? tipo;
}
