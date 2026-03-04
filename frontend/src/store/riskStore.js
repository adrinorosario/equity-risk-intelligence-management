/**
 * Risk Zustand store.
 */

import { create } from "zustand";
import { httpClient } from "../api/httpClient";
import { endpoints } from "../api/endpoints";

export const useRiskStore = create((set) => ({
  assessments: [],
  metrics: [],
  loading: false,

  loadMetrics: async () => {
    try {
      const { data } = await httpClient.get(endpoints.risk.metrics);
      set({ metrics: data });
    } catch {
      set({ metrics: [] });
    }
  },

  loadAssessments: async (portfolioId) => {
    set({ loading: true });
    try {
      const { data } = await httpClient.get(endpoints.risk.assessments, {
        params: { portfolio_id: portfolioId },
      });
      set({ assessments: data, loading: false });
    } catch {
      set({ assessments: [], loading: false });
    }
  },

  assessEquity: async (payload) => {
    const { data } = await httpClient.post(endpoints.risk.assess, payload);
    set((s) => ({ assessments: [...s.assessments, data] }));
    return data;
  },
}));
