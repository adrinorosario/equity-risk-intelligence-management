# ERIMS - Project Implementation Details & Directory Roadmap

This document provides a comprehensive mapping of the **Equity Risk Intelligent Management System (ERIMS)** Software Requirements Specification (SRS) to the existing codebase structure. It serves as a checklist and guide for all engineers to understand what needs to be implemented in each directory and file.

---

## 🏗️ Project Architecture Overview
- **Backend**: FastAPI (Python) with SQLAlchemy ORM and PostgreSQL.
- **Frontend**: React (Vite, TailwindCSS) with Zustand for state management.
- **Database**: PostgreSQL for relational data (relational integrity per NFR3).

---

## 📂 Backend (FastAPI) Implementation Roadmap

### 📂 `backend/app/db/`
Database connection, session management, and SQLAlchemy models.
- [ ] **`backend/app/db/postgres.py`**: Configure SQLAlchemy engine and session factory.
- [ ] **`backend/app/db/models/`**:
    - [ ] **`base.py`**: Add naming conventions for Alembic migrations.
    - [ ] **`user.py`** (to be created): Implement `User` model with `user_id`, `name`, `email`, `role` (FR6), `password_hash` (NFR1).
    - [ ] **`portfolio.py`** (to be created): Implement `Portfolio` model with `portfolio_id`, `user_id` (FK), `portfolio_name`, `total_value`, `risk_level`.
    - [ ] **`equity.py`** (to be created): Implement `Equity` model with `equity_id`, `portfolio_id` (FK), `company_name`, `sector`, `market_value` (FR3).
    - [ ] **`risk.py`** (to be created): Implement `RiskMetric` and `RiskAssessment` models per Task 2 of SRS.
- [ ] **`backend/app/db/migrations/`**: Manage database schema versions via Alembic.

### 📂 `backend/app/schemas/`
Pydantic models for request/response validation.
- [ ] **`user.py`**: `UserCreate`, `UserUpdate`, `UserPublic`.
- [ ] **`portfolio.py`**: `PortfolioCreate`, `PortfolioPublic`, `PortfolioUpdate`.
- [ ] **`equity.py`**: `EquityCreate`, `EquityPublic`.
- [ ] **`risk.py`**: `RiskMetricCreate`, `RiskAssessmentPublic`.
- [ ] **`report.py`**: `ReportPublic` for risk evaluation summaries.

### 📂 `backend/app/api/v1/endpoints/`
API Route controllers. All routes should implement authentication (NFR1).
- [ ] **`auth.py`**: `POST /register`, `POST /login` (JWT token issuance per FR1).
- [ ] **`users.py`**: `GET /me`, `PUT /profile` (Profile management per FR1).
- [ ] **`portfolios.py`**: CRUD for user portfolios (FR2).
- [ ] **`equities.py`**: Manage equities within a portfolio (FR3).
- [ ] **`risk.py`**: Compute and retrieve risk metrics (FR4).
- [ ] **`reports.py`**: Generate and retrieve risk evaluation reports (FR5).

### 📂 `backend/app/services/`
Core business logic layer.
- [ ] **`auth_service.py`**: Secure password hashing (NFR1) and token validation.
- [ ] **`portfolio_service.py`**: Logic for managing portfolios and aggregating total values.
- [ ] **`risk_service.py`**: Orchestrate risk calculations by calling the `engine`.
- [ ] **`report_service.py`**: Aggregate risk scores and generate PDF/JSON summaries.

### 📂 `backend/app/engine/`
Computational core for risk analysis (FR4).
- [ ] **`risk/metrics.py`**: Implement math for Market Exposure and Risk Scores.
- [ ] **`forecasting/volatility.py`**: Implement volatility calculation (Standard Deviation, Beta, etc.).
- [ ] **`data/market_data.py`**: Logic for collecting/fetching market data (to be stored in the DB).
- [ ] **`monitoring/alerts.py`**: Check risk thresholds and trigger notifications.

---

## 🎨 Frontend (React) Implementation Roadmap

### 📂 `frontend/src/api/`
- [ ] **`httpClient.js`**: Configure Axios instance with JWT interceptors for security (NFR1).
- [ ] **`endpoints.js`**: Define constants for all backend API routes.

### 📂 `frontend/src/store/`
Zustand state management.
- [ ] **`authStore.js`**: Handle user session, login status, and role-based access (Investor vs. Analyst).
- [ ] **`index.js`**: Centralize stores (PortfolioStore, RiskStore).

### 📂 `frontend/src/features/`
- [ ] **`auth/`**:
    - [ ] **`LoginPage.jsx`**: Form for login with validation.
    - [ ] **`RegisterPage.jsx`**: User registration form.
- [ ] **`portfolio/`**:
    - [ ] **`PortfolioListPage.jsx`**: View portfolios, add/delete, and view summary metrics (FR2).
    - [ ] **`PortfolioDetailsPage.jsx`** (to be created): Manage individual equities (FR3).
- [ ] **`risk/`**:
    - [ ] **`RiskDashboardPage.jsx`**: Visual dashboard for risk metrics (Volatility, Exposure charts) (FR4).
- [ ] **`reports/`**:
    - [ ] **`ReportsPage.jsx`**: UI to generate and download risk reports (FR5).

### 📂 `frontend/src/components/`
- [ ] **Shared UI Components**: `Layout`, `Sidebar`, `Button`, `Input`, `RiskChart`.

---

## ✅ Implementation Checklist (Priority Order)

1.  **Phase 1: Foundation (Security & Data)**
    - [ ] Setup PostgreSQL and Alembic migrations.
    - [ ] Implement `User` model and `AuthService` (Hashing, JWT).
    - [ ] Implement Register/Login UI in Frontend.
2.  **Phase 2: Core Features (Portfolios & Equities)**
    - [ ] Implement CRUD for Portfolios and Equities (Backend + Frontend).
    - [ ] Setup relational integrity (Equities must belong to Portfolios).
3.  **Phase 3: Intelligence (Risk Engine)**
    - [ ] Implement Volatility and Risk Score logic in `backend/app/engine/`.
    - [ ] Create `risk_service` to compute and store assessments.
    - [ ] Build the Risk Dashboard UI in Frontend.
4.  **Phase 4: Reporting & Roles**
    - [ ] Implement Role-based access (Investor views only their data; Analyst views across users if needed).
    - [ ] Generate Risk Reports (Backend logic + UI Page).
5.  **Phase 5: Performance & Optimization (NFR2)**
    - [ ] Optimize database queries and risk calculations to ensure < 3s response time.
