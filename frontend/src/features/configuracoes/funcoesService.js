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

export async function listarFuncoes(config = {}) {
  const response = await api.get("/funcoes", config);
  return normalizarLista(response.data);
}

export async function criarFuncao(payload, config = {}) {
  const response = await api.post("/funcoes", payload, config);
  return response.data;
}

export async function atualizarFuncao(id, payload, config = {}) {
  const response = await api.put(`/funcoes/${id}`, payload, config);
  return response.data;
}

export async function ativarFuncao(id, config = {}) {
  const response = await api.patch(`/funcoes/${id}/ativar`, null, config);
  return response.data;
}

export async function desativarFuncao(id, config = {}) {
  const response = await api.patch(`/funcoes/${id}/desativar`, null, config);
  return response.data;
}
