import { api } from "../../services/api";

export async function buscarEvolucaoColaborador(colaboradorId, { signal } = {}) {
  const response = await api.get(`/colaboradores/${colaboradorId}/evolucao`, { signal });
  return response.data;
}
