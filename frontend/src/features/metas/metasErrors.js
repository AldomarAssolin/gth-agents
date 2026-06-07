export function getMetaErrorMessage(error) {
  if (!error.response) {
    return "Não foi possível conectar à API.";
  }

  const status = error.response.status;
  const apiMessage = error.response.data?.message || error.response.data?.error;

  if (typeof apiMessage === "string" && apiMessage.trim()) {
    return apiMessage;
  }

  if (status === 400 || status === 422) {
    return "Dados inválidos.";
  }
  if (status === 403) {
    return "Você não possui permissão para executar esta ação.";
  }
  if (status === 404) {
    return "Recurso não encontrado.";
  }
  
  return "Ocorreu um erro inesperado.";
}
