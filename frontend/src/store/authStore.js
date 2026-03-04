/**
 * Auth state store (token/user/session management).
 */

import { create } from "zustand";
import { httpClient } from "../api/httpClient";
import { endpoints } from "../api/endpoints";

export const useAuthStore = create((set, get) => ({
  accessToken: globalThis.localStorage.getItem("accessToken"),
  currentUser: null,
  loading: false,

  login: async (email, password) => {
    const response = await httpClient.post(endpoints.auth.login, { email, password });
    const { access_token: token } = response.data;
    globalThis.localStorage.setItem("accessToken", token);
    set({ accessToken: token });
    await get().loadCurrentUser();
  },

  register: async (payload) => {
    await httpClient.post(endpoints.auth.register, payload);
  },

  loadCurrentUser: async () => {
    try {
      set({ loading: true });
      const { data } = await httpClient.get(endpoints.users.me);
      set({ currentUser: data, loading: false });
    } catch (err) {
      set({ loading: false });
      throw new Error("Failed to load user");
    }
  },

  logout: () => {
    globalThis.localStorage.removeItem("accessToken");
    set({ accessToken: null, currentUser: null });
  },
}));
