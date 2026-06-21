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

export async function listarSetores(config = {}) {
  const response = await api.get("/setores", config);
  return normalizarLista(response.data);
}

export async function criarSetor(payload, config = {}) {
  const response = await api.post("/setores", payload, config);
  return response.data;
}

export async function atualizarSetor(id, payload, config = {}) {
  const response = await api.put(`/setores/${id}`, payload, config);
  return response.data;
}

export async function ativarSetor(id, config = {}) {
  const response = await api.patch(`/setores/${id}/ativar`, null, config);
  return response.data;
}

export async function desativarSetor(id, config = {}) {
  const response = await api.patch(`/setores/${id}/desativar`, null, config);
  return response.data;
}
