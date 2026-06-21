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

export async function listarUsuarios(config = {}) {
  const response = await api.get("/usuarios", config);
  return normalizarLista(response.data);
}

export async function criarUsuario(payload, config = {}) {
  const response = await api.post("/usuarios", payload, config);
  return response.data;
}

export async function atualizarUsuario(id, payload, config = {}) {
  const response = await api.put(`/usuarios/${id}`, payload, config);
  return response.data;
}

export async function ativarUsuario(id, config = {}) {
  const response = await api.patch(`/usuarios/${id}/ativar`, null, config);
  return response.data;
}

export async function desativarUsuario(id, config = {}) {
  const response = await api.patch(`/usuarios/${id}/desativar`, null, config);
  return response.data;
}
