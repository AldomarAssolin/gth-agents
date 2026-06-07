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
