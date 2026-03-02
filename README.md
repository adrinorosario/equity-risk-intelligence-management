<!--
TLDR; Monorepo scaffold for ERIMS (React + FastAPI) with Postgres + Mongo provisions.
TODO: Implement domain logic (auth/portfolio/risk/reporting) and analytics engine (forecasting/optimization/monitoring).
-->

## Equity Risk Intelligent Management System (ERIMS)

This repository is a **starter project structure** aligned to `SRS.pdf`:

- **Frontend**: React (Vite) for dashboards, forms, and reporting UI
- **Backend**: FastAPI for REST APIs, auth, orchestration of analytics jobs
- **Datastores**: PostgreSQL (relational portfolio + risk tables) and MongoDB (document/time-series style data)
- **Analytics engine**: Python package area for risk analysis, forecasting, optimization, and monitoring (no implementations yet)

## Repository layout

```text
.
├── docker-compose.yml
├── .env.example
├── .gitignore
├── Makefile
├── frontend/
└── backend/
    ├── alembic.ini
    ├── pyproject.toml
    ├── requirements.txt
    ├── app/
    ├── tests/
    └── infra/
        ├── postgres/
        └── mongo/
```

## Quickstart (local dev)

### Prereqs

- Node.js 18+
- Python 3.11+
- Docker Desktop

### 1) Start databases

```bash
cp .env.example .env
docker compose up -d
```

### 2) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3) Frontend

```bash
cd frontend
npm install
npm run dev
```

## Notes on Postgres vs MongoDB

- **PostgreSQL (recommended for)**: Users, portfolios, equities, risk metric definitions, assessments, reporting metadata.
- **MongoDB (recommended for)**: Raw market data snapshots, news/sentiment documents, feature store artifacts, model runs, time-series monitoring events.

Both are provisioned in `docker-compose.yml`; wiring is stubbed in `backend/app/db/postgres.py` and `backend/app/db/mongo.py`.