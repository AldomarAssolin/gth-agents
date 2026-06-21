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

export async function listarCompetencias(config = {}) {
  const response = await api.get("/competencias", config);
  return normalizarLista(response.data);
}

export async function criarCompetencia(payload, config = {}) {
  const response = await api.post("/competencias", payload, config);
  return response.data;
}

export async function atualizarCompetencia(id, payload, config = {}) {
  const response = await api.put(`/competencias/${id}`, payload, config);
  return response.data;
}

export async function ativarCompetencia(id, config = {}) {
  const response = await api.patch(`/competencias/${id}/ativar`, null, config);
  return response.data;
}

export async function desativarCompetencia(id, config = {}) {
  const response = await api.patch(`/competencias/${id}/desativar`, null, config);
  return response.data;
}
