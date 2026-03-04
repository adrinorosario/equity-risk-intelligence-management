# TLDR; Convenience commands for local development.
# TODO: Extend with CI/test/lint commands as you add workflows.

.PHONY: help up down backend frontend

help:
	@echo "Targets:"
	@echo "  up       - start Postgres + Mongo"
	@echo "  down     - stop containers"
	@echo "  backend  - run FastAPI in reload mode"
	@echo "  frontend - run React dev server"

up:
	docker compose up -d

down:
	docker compose down

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev
