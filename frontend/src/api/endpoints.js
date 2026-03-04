/**
 * Centralized API endpoint path helpers.
 */

export const endpoints = {
  auth: {
    login: "/auth/login",
    register: "/auth/register",
  },
  users: {
    me: "/users/me",
  },
  portfolios: {
    list: "/portfolios",
    create: "/portfolios",
    detail: (id) => `/portfolios/${id}`,
    update: (id) => `/portfolios/${id}`,
    delete: (id) => `/portfolios/${id}`,
    equities: (id) => `/portfolios/${id}/equities`,
  },
  equities: {
    update: (id) => `/equities/${id}`,
    delete: (id) => `/equities/${id}`,
  },
  risk: {
    assess: "/risk/assess",
    assessments: "/risk/assessments",
    metrics: "/risk/metrics",
  },
  reports: {
    create: "/reports",
    list: "/reports",
  },
};
