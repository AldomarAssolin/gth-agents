import axios from "axios";
import { getToken } from "../features/auth/authStorage";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      if (!config.headers) {
        config.headers = {};
      }
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const { response, config } = error;
    
    if (response && response.status === 401) {
      const isLoginUrl = config && config.url && (config.url.endsWith("/auth/login") || config.url.includes("/auth/login"));
      if (!isLoginUrl) {
        window.dispatchEvent(new CustomEvent("auth:unauthorized"));
      }
    }
    
    return Promise.reject(error);
  }
);
