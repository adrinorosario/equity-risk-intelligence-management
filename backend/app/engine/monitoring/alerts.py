# TLDR; Alerting scaffolds (threshold checks, anomaly flags) — scaffold only.
# TODO: Implement rule evaluation and persistence (Mongo recommended for events).

import pandas as pd
from sklearn.ensemble import IsolationForest

from app.core.exceptions import NotImplementedFeatureError


class AlertingEngine:
    def evaluate(self, series: pd.Series) -> dict[str, str]:
        raise NotImplementedFeatureError("evaluate not implemented")
