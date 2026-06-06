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

export async function listarColaboradores(config = {}) {
  const response = await api.get("/colaboradores", config);
  return normalizarLista(response.data);
}

export async function buscarColaboradorPorId(id, config = {}) {
  const response = await api.get(`/colaboradores/${id}`, config);
  return response.data;
}

export async function criarColaborador(payload, config = {}) {
  const response = await api.post("/colaboradores", payload, config);
  return response.data;
}

export async function listarSetores(config = {}) {
  const response = await api.get("/setores", config);
  return normalizarLista(response.data);
}

export async function listarFuncoes(config = {}) {
  const response = await api.get("/funcoes", config);
  return normalizarLista(response.data);
}
