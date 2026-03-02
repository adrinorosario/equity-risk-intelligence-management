<!--
TLDR; FastAPI backend + analytics engine scaffold for ERIMS.
TODO: Implement endpoints/services, define DB models/migrations, and build the analytical engine modules.
-->

## Backend

Run locally (after `pip install -r requirements.txt`):

```bash
uvicorn app.main:app --reload
```

Key directories:

- `app/api/`: versioned FastAPI routers (structure only)
- `app/services/`: use-case orchestration (structure only)
- `app/db/`: Postgres/Mongo wiring + migrations scaffold
- `app/engine/`: analytics engine namespaces (risk/forecasting/optimization/monitoring)
