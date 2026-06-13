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

export async function listarPDIs(options = {}) {
  const response = await api.get("/pdis", options);
  return normalizarLista(response.data);
}

export async function buscarPDI(pdiId, options = {}) {
  const response = await api.get(`/pdis/${pdiId}`, options);
  return response.data;
}

export async function criarPDI(payload, options = {}) {
  const response = await api.post("/pdis", payload, options);
  return response.data;
}

export async function atualizarPDI(pdiId, payload, options = {}) {
  const response = await api.patch(`/pdis/${pdiId}`, payload, options);
  return response.data;
}

export async function concluirPDI(pdiId, options = {}) {
  const response = await api.patch(`/pdis/${pdiId}/concluir`, {}, options);
  return response.data;
}

export async function cancelarPDI(pdiId, options = {}) {
  const response = await api.patch(`/pdis/${pdiId}/cancelar`, {}, options);
  return response.data;
}

export async function listarPDIsPorColaborador(colaboradorId, options = {}) {
  const response = await api.get(`/colaboradores/${colaboradorId}/pdis`, options);
  return normalizarLista(response.data);
}

export async function criarAcaoPDI(pdiId, payload, options = {}) {
  const response = await api.post(`/pdis/${pdiId}/acoes`, payload, options);
  return response.data;
}

export async function atualizarAcaoPDI(pdiId, acaoId, payload, options = {}) {
  const response = await api.patch(`/pdis/${pdiId}/acoes/${acaoId}`, payload, options);
  return response.data;
}

export async function concluirAcaoPDI(pdiId, acaoId, options = {}) {
  const response = await api.patch(`/pdis/${pdiId}/acoes/${acaoId}/concluir`, {}, options);
  return response.data;
}

export async function cancelarAcaoPDI(pdiId, acaoId, options = {}) {
  const response = await api.patch(`/pdis/${pdiId}/acoes/${acaoId}/cancelar`, {}, options);
  return response.data;
}
