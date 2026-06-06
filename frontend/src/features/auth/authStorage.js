export function saveToken(token) {
  if (token) {
    localStorage.setItem("access_token", token);
  }
}

export function getToken() {
  return localStorage.getItem("access_token");
}

export function removeToken() {
  localStorage.removeItem("access_token");
}

export function saveUser(user) {
  if (user) {
    localStorage.setItem("current_user", JSON.stringify(user));
  }
}

export function getUser() {
  const value = localStorage.getItem("current_user");
  if (!value) {
    return null;
  }
  try {
    return JSON.parse(value);
  } catch {
    localStorage.removeItem("current_user");
    return null;
  }
}

export function removeUser() {
  localStorage.removeItem("current_user");
}

export function clearAuthStorage() {
  removeToken();
  removeUser();
}

export function decodeJwt(token) {
  if (!token) return null;
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    
    let base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
    const pad = base64.length % 4;
    if (pad) {
      if (pad === 1) return null;
      base64 += '='.repeat(4 - pad);
    }
    
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

export function isTokenExpired(token) {
  if (!token) return true;
  const payload = decodeJwt(token);
  if (!payload) {
    // token malformado -> inválido (true)
    return true;
  }
  if (payload.exp === undefined) {
    // token sem exp -> deixar a API validar (false)
    return false;
  }
  const currentTime = Date.now() / 1000;
  return payload.exp < currentTime;
}
