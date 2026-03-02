/**
 * TLDR; Auth state store scaffold (token/user/session).
 * TODO: Implement login/logout, token storage, and user profile loading.
 */

import { create } from "zustand";

export const useAuthStore = create(() => ({
  accessToken: null,
  currentUser: null
}));

