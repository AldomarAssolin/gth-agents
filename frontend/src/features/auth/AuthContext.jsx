/* eslint-disable react-refresh/only-export-components */
import { createContext, useState, useEffect } from "react";
import * as authStorage from "./authStorage";
import * as authService from "./authService";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => authStorage.getToken());
  const [user, setUser] = useState(() => authStorage.getUser());
  const [isInitializing, setIsInitializing] = useState(true);

  const logout = () => {
    authStorage.clearAuthStorage();
    setToken(null);
    setUser(null);
    authService.logout().catch(() => {});
  };

  const login = async (email, senha) => {
    const result = await authService.login(email, senha);
    authStorage.saveToken(result.token);
    authStorage.saveUser(result.user);
    setToken(result.token);
    setUser(result.user);
    return result;
  };

  useEffect(() => {
    const initAuth = () => {
      const storedToken = authStorage.getToken();
      if (storedToken) {
        if (authStorage.isTokenExpired(storedToken)) {
          authStorage.clearAuthStorage();
          setToken(null);
          setUser(null);
        }
      } else {
        // Se access_token não existir, current_user deve ser removido se estiver órfão
        authStorage.removeUser();
        setUser(null);
      }
      setIsInitializing(false);
    };

    initAuth();
  }, []);

  useEffect(() => {
    const handleUnauthorized = () => {
      logout();
    };

    window.addEventListener("auth:unauthorized", handleUnauthorized);
    return () => {
      window.removeEventListener("auth:unauthorized", handleUnauthorized);
    };
  }, []);

  const isAuthenticated = Boolean(token);

  const value = {
    user,
    token,
    isAuthenticated,
    isInitializing,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
