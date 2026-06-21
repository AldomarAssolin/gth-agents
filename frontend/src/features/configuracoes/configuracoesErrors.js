export function getConfiguracoesErrorMessage(error) {
  const status = error.response?.status;

  const apiMessage =
    error.response?.data?.message ??
    error.response?.data?.error_description;

  if (typeof apiMessage === "string" && apiMessage.trim()) {
    return apiMessage;
  }

  const messages = {
    400: "Verifique os dados informados.",
    401: "Sua sessão expirou. Faça login novamente.",
    403: "Você não possui permissão para realizar esta operação.",
    404: "O recurso solicitado não foi encontrado.",
    409: "Já existe um registro conflitante com estes dados.",
    500: "Ocorreu um erro interno no servidor.",
  };

  if (!error.response) {
    return "Não foi possível conectar ao servidor.";
  }

  return messages[status] ?? "Não foi possível concluir a operação.";
}
