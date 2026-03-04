/**
 * Axios HTTP client wrapper for backend API.
 * Handles JWT injection and 401 auto-logout.
 */

import axios from "axios";

export const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  timeout: 30_000,
});

// Inject bearer token on every request
httpClient.interceptors.request.use((config) => {
  const token = globalThis.localStorage.getItem("accessToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-logout on 401
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      globalThis.localStorage.removeItem("accessToken");
      if (!["/login", "/register"].includes(globalThis.location.pathname)) {
        globalThis.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);
