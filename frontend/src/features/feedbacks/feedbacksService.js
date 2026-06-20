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

export async function criarFeedback(payload, options = {}) {
  const response = await api.post("/feedbacks", payload, options);
  return response.data;
}

export async function listarFeedbacksPorColaborador(colaboradorId, options = {}) {
  const response = await api.get(`/colaboradores/${colaboradorId}/evolucao`, options);
  return normalizarLista(response.data?.feedbacks);
}
