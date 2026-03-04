/**
 * Route table for ERIMS frontend.
 */

import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { ProtectedRoute } from "../components/ProtectedRoute.jsx";
import { LoginPage } from "../features/auth/LoginPage.jsx";
import { RegisterPage } from "../features/auth/RegisterPage.jsx";
import { PortfolioListPage } from "../features/portfolio/PortfolioListPage.jsx";
import { PortfolioDetailsPage } from "../features/portfolio/PortfolioDetailsPage.jsx";
import { RiskDashboardPage } from "../features/risk/RiskDashboardPage.jsx";
import { ReportsPage } from "../features/reports/ReportsPage.jsx";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/portfolios" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/portfolios"
        element={<ProtectedRoute><PortfolioListPage /></ProtectedRoute>}
      />
      <Route
        path="/portfolios/:id"
        element={<ProtectedRoute><PortfolioDetailsPage /></ProtectedRoute>}
      />
      <Route
        path="/risk"
        element={<ProtectedRoute><RiskDashboardPage /></ProtectedRoute>}
      />
      <Route
        path="/reports"
        element={<ProtectedRoute><ReportsPage /></ProtectedRoute>}
      />
    </Routes>
  );
}
