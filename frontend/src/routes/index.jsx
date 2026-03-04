/**
 * TLDR; Route table for ERIMS frontend.
 * TODO: Add pages for auth, portfolio management, risk dashboards, and reporting.
 */

import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { LoginPage } from "../features/auth/LoginPage.jsx";
import { RegisterPage } from "../features/auth/RegisterPage.jsx";
import { PortfolioListPage } from "../features/portfolio/PortfolioListPage.jsx";
import { RiskDashboardPage } from "../features/risk/RiskDashboardPage.jsx";
import { ReportsPage } from "../features/reports/ReportsPage.jsx";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/portfolios" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/portfolios" element={<PortfolioListPage />} />
      <Route path="/risk" element={<RiskDashboardPage />} />
      <Route path="/reports" element={<ReportsPage />} />
    </Routes>
  );
}

