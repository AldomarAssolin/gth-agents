import { api } from "../../services/api";
import { decodeJwt, getUser, getToken as getStoredToken } from "./authStorage";

export async function login(email, senha) {
  const response = await api.post("/auth/login", { email, senha });
  const { access_token, usuario } = response.data;

  let normalizedUser = null;
  if (usuario) {
    normalizedUser = {
      id: usuario.id !== undefined ? usuario.id : null,
      nome: usuario.nome || null,
      email: usuario.email || null,
      perfil: usuario.perfil || null,
      colaborador_id: usuario.colaborador_id !== undefined ? usuario.colaborador_id : null,
      setor_id: usuario.setor_id !== undefined ? usuario.setor_id : null,
    };
  } else if (access_token) {
    const payload = decodeJwt(access_token);
    if (payload) {
      normalizedUser = {
        id: payload.id !== undefined ? payload.id : null,
        nome: payload.nome || payload.email || null,
        email: payload.email || null,
        perfil: payload.perfil || null,
        colaborador_id: payload.colaborador_id !== undefined ? payload.colaborador_id : null,
        setor_id: payload.setor_id !== undefined ? payload.setor_id : null,
      };
    }
  }

  return {
    token: access_token,
    user: normalizedUser,
  };
}

export async function logout() {
  return true;
}

export function getCurrentUser() {
  return getUser();
}

export function getToken() {
  return getStoredToken();
}
