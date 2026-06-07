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

export async function criarMeta(payload, options = {}) {
  const response = await api.post("/metas", payload, options);
  return response.data;
}

export async function listarMetasPorColaborador(colaboradorId, options = {}) {
  const response = await api.get(`/colaboradores/${colaboradorId}/metas`, options);
  return normalizarLista(response.data);
}
