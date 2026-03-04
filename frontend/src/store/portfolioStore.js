/**
 * Portfolio & equity Zustand store.
 */

import { create } from "zustand";
import { httpClient } from "../api/httpClient";
import { endpoints } from "../api/endpoints";

export const usePortfolioStore = create((set) => ({
  portfolios: [],
  currentPortfolio: null,
  equities: [],
  loading: false,
  error: null,

  loadPortfolios: async () => {
    set({ loading: true, error: null });
    try {
      const { data } = await httpClient.get(endpoints.portfolios.list);
      set({ portfolios: data, loading: false });
    } catch (err) {
      set({ error: "Failed to load portfolios", loading: false });
    }
  },

  loadPortfolio: async (id) => {
    set({ loading: true, error: null });
    try {
      const { data } = await httpClient.get(endpoints.portfolios.detail(id));
      set({ currentPortfolio: data, loading: false });
    } catch (err) {
      set({ error: "Failed to load portfolio", loading: false });
    }
  },

  createPortfolio: async (payload) => {
    const { data } = await httpClient.post(endpoints.portfolios.create, {
      ...payload,
      user_id: 0, // server overrides with auth'd user
    });
    set((s) => ({ portfolios: [...s.portfolios, data] }));
    return data;
  },

  updatePortfolio: async (id, payload) => {
    const { data } = await httpClient.put(endpoints.portfolios.update(id), payload);
    set((s) => ({
      portfolios: s.portfolios.map((p) => (p.portfolio_id === id ? data : p)),
      currentPortfolio: s.currentPortfolio?.portfolio_id === id ? data : s.currentPortfolio,
    }));
    return data;
  },

  deletePortfolio: async (id) => {
    await httpClient.delete(endpoints.portfolios.delete(id));
    set((s) => ({
      portfolios: s.portfolios.filter((p) => p.portfolio_id !== id),
    }));
  },

  loadEquities: async (portfolioId) => {
    set({ loading: true });
    try {
      const { data } = await httpClient.get(endpoints.portfolios.equities(portfolioId));
      set({ equities: data, loading: false });
    } catch {
      set({ equities: [], loading: false });
    }
  },

  addEquity: async (portfolioId, payload) => {
    const { data } = await httpClient.post(endpoints.portfolios.equities(portfolioId), {
      ...payload,
      portfolio_id: portfolioId,
    });
    set((s) => ({ equities: [...s.equities, data] }));
    return data;
  },

  updateEquity: async (equityId, payload) => {
    const { data } = await httpClient.put(endpoints.equities.update(equityId), payload);
    set((s) => ({
      equities: s.equities.map((e) => (e.equity_id === equityId ? data : e)),
    }));
  },

  deleteEquity: async (equityId) => {
    await httpClient.delete(endpoints.equities.delete(equityId));
    set((s) => ({
      equities: s.equities.filter((e) => e.equity_id !== equityId),
    }));
  },
}));
