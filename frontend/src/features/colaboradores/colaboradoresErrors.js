export function getColaboradorErrorMessage(error) {
  const status = error.response?.status;

  const apiMessage =
    error.response?.data?.message ??
    error.response?.data?.error_description;

  if (typeof apiMessage === "string" && apiMessage.trim()) {
    return apiMessage;
  }

  const messages = {
    400: "Verifique os dados informados.",
    403: "Você não possui permissão para realizar esta operação.",
    404: "Colaborador, setor ou função não encontrado.",
    409: "Já existe um colaborador com esta matrícula ou e-mail.",
  };

  if (!error.response) {
    return "Não foi possível conectar ao servidor.";
  }

  return messages[status] ?? "Não foi possível concluir a operação.";
}
