/**
 * TLDR; Axios HTTP client wrapper for backend API.
 * TODO: Add auth token injection, refresh handling, and consistent error mapping.
 */

import axios from "axios";

export const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  timeout: 30_000
});

httpClient.interceptors.request.use((config) => {
  const token = window.localStorage.getItem("accessToken");
  if (token) {
    // eslint-disable-next-line no-param-reassign
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

