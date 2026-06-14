import { api } from "../../services/api";

function normalizarLista(data) {
  if (Array.isArray(data)) {
    return data;
  }
  if (Array.isArray(data?.items)) {
    return data.items;
  }
  if (Array.isArray(data?.data)) {
    return data.data;
  }
  return [];
}

export async function listarReconhecimentos(options = {}) {
  const response = await api.get("/reconhecimentos", options);
  return normalizarLista(response.data);
}

export async function criarReconhecimento(payload, options = {}) {
  const response = await api.post("/reconhecimentos", payload, options);
  return response.data;
}

export async function cancelarReconhecimento(id, motivo, options = {}) {
  const response = await api.patch(`/reconhecimentos/${id}/cancelar`, { motivo_cancelamento: motivo }, options);
  return response.data;
}

export async function listarReconhecimentosPorColaborador(colaboradorId, options = {}) {
  const response = await api.get(`/colaboradores/${colaboradorId}/reconhecimentos`, options);
  return normalizarLista(response.data);
}
