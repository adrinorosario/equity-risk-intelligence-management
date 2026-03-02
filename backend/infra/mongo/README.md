<!--
TLDR; MongoDB provisioning notes for ERIMS (collections, indexes, document shapes).
TODO: Decide which datasets live in Mongo (e.g., market data snapshots, model artifacts, monitoring events).
-->

Suggested collections (non-binding):

- `market_prices`: price snapshots/time-series
- `news_events`: unstructured news/sentiment payloads
- `feature_store`: engineered features keyed by (symbol, date)
- `model_runs`: training/inference metadata + metrics
- `alerts`: monitoring events and anomaly flags
