/**
 * TLDR; Centralized API endpoint path helpers.
 * TODO: Keep endpoints aligned with backend versioning (`/api/v1`).
 */

export const endpoints = {
  auth: {
    login: "/auth/login",
    register: "/auth/register"
  },
  users: "/users",
  portfolios: "/portfolios",
  equities: "/equities",
  risk: "/risk",
  reports: "/reports"
};

