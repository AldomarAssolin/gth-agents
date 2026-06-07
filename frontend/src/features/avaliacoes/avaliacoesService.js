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

export async function criarAvaliacao(payload, config = {}) {
  const response = await api.post("/avaliacoes", payload, config);
  return response.data;
}

export async function listarCompetencias(config = {}) {
  const response = await api.get("/competencias", config);
  return normalizarLista(response.data);
}
