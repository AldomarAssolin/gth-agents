export function resolverNomeSetor(colaborador, setores) {
  if (!colaborador) return "Não informado";
  if (colaborador.setor?.nome) {
    return colaborador.setor.nome;
  }

  const setor = (setores || []).find(
    (item) => Number(item.id) === Number(colaborador.setor_id)
  );

  if (setor?.nome) {
    return setor.nome;
  }

  if (colaborador.setor_id) {
    return `Setor #${colaborador.setor_id}`;
  }

  return "Não informado";
}

export function resolverNomeFuncao(colaborador, funcoes) {
  if (!colaborador) return "Não informado";
  if (colaborador.funcao?.nome) {
    return colaborador.funcao.nome;
  }

  const funcao = (funcoes || []).find(
    (item) => Number(item.id) === Number(colaborador.funcao_id)
  );

  if (funcao?.nome) {
    return funcao.nome;
  }

  if (colaborador.funcao_id) {
    return `Função #${colaborador.funcao_id}`;
  }

  return "Não informado";
}

export function formatarDataBrasil(value) {
  if (!value) {
    return "Não informado";
  }

  const datePart = String(value).slice(0, 10);
  const [year, month, day] = datePart.split("-");

  if (!year || !month || !day) {
    return "Não informado";
  }

  return `${day}/${month}/${year}`;
}
