/**
 * TLDR; Auth state store scaffold (token/user/session).
 * TODO: Implement login/logout, token storage, and user profile loading.
 */

import { create } from "zustand";
import { httpClient } from "../api/httpClient";
import { endpoints } from "../api/endpoints";

export const useAuthStore = create((set) => ({
  accessToken: window.localStorage.getItem("accessToken"),
  currentUser: null,

  login: async (email, password) => {
    const response = await httpClient.post(endpoints.auth.login, { email, password });
    const { access_token: token } = response.data;
    window.localStorage.setItem("accessToken", token);
    set({ accessToken: token });
    await useAuthStore.getState().loadCurrentUser();
  },

  register: async (payload) => {
    await httpClient.post(endpoints.auth.register, payload);
  },

  loadCurrentUser: async () => {
    const { data } = await httpClient.get(`${endpoints.users}/me`);
    set({ currentUser: data });
  },

  logout: () => {
    window.localStorage.removeItem("accessToken");
    set({ accessToken: null, currentUser: null });
  }
}));

