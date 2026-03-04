## Equity Risk Analytics Engine — Build Roadmap

This roadmap assumes ~4 hours of focused work and that you will **only work inside the analytics engine layer** (`backend/app/engine/**`) so it can later be wired into the backend APIs. Each task has a checkbox, goal, target file, and concrete actions. Work roughly top‑to‑bottom; skip “Stretch” tasks if you run out of time.

---

## Phase 0 — Understand Requirements & Architecture (10–20 min)

- [ ] **0.1 Read SRS and map to engine responsibilities**  
  - **Goal**: Align the engine with SRS functional requirements (FR4, FR5) and entities (User, Portfolio, Equity, Risk_Assessment, Risk_Metric).  
  - **Files**: `SRS.pdf` (read only), `engine_specs.md` (this file).  
  - **What to do**:  
    - Skim SRS sections: Problem Statement, Scope, FR4 (Risk Assessment), FR5 (Reporting), EER diagram.  
    - Note that **backend + DB** will handle Users/Portfolios/Equities; your engine should:  
      - Take **historical prices and positions** as inputs.  
      - Compute **risk metrics** (volatility, exposure, concentration, risk scores) per equity and per portfolio.  
      - **Forecast** risk (future volatility / risk scores).  
      - **Optimize** portfolios (target weights) and return diagnostics for reports.  
    - Jot a quick mapping:  
      - *Equity → price history + risk metrics*  
      - *Portfolio → holdings + aggregated risk metrics + optimization*  

- [ ] **0.2 Decide minimal “MVP path” you’ll implement in 4 hours**  
  - **Goal**: Be realistic so you have a working end‑to‑end flow rather than many half‑finished pieces.  
  - **Files**: `engine_specs.md`.  
  - **What to do**:  
    - Commit to this minimal MVP:  
      - From price history → compute **daily returns**.  
      - From returns → compute **current volatility** and a **simple volatility forecast**.  
      - From positions → compute **exposure** and **concentration**.  
      - From prices → compute **mean/variance** and run a basic **mean–variance optimization** using `PortfolioOptimizer`.  
      - Bundle all results into a **plain Python dict** that the backend can serialize into JSON and store as `Risk_Assessment` / `Risk_Metric` rows.  

---

## Phase 1 — Define Clean Engine Interfaces (20–30 min)

Focus: make clear, backend‑friendly function signatures. You are **not** implementing any backend routes; only analytics.

- [ ] **1.1 Define engine‑wide data contracts (types & docstrings)**  
  - **Goal**: Decide what data structures your engine expects/returns so backend devs know how to call it.  
  - **Files**:  
    - `backend/app/engine/__init__.py`  
    - `backend/app/engine/data/__init__.py`  
    - `backend/app/engine/risk/__init__.py`  
    - `backend/app/engine/forecasting/__init__.py`  
    - `backend/app/engine/optimization/__init__.py`  
    - `backend/app/engine/pipelines/__init__.py`  
  - **What to do**:  
    - Open each `__init__.py` and add **high‑level docstrings** that describe the module role (e.g., data access, risk metrics, forecasting, optimization, orchestration).  
    - In `backend/app/engine/__init__.py`, add documentation describing:  
      - The conceptual flow: *market data → features/returns → risk metrics & forecasts → optimization → report‑ready dicts*.  
      - That all public functions should be **pure analytics**: they accept pandas objects / simple dicts, and return pandas/NumPy or serializable dicts.  
    - Optionally define simple type aliases (in a convenient module, e.g. `backend/app/engine/__init__.py`):  
      - `PriceHistory = pd.DataFrame` (index = dates, columns = tickers).  
      - `Returns = pd.DataFrame` (same shape).  
      - `Positions = pd.DataFrame` (columns like `symbol`, `shares`, `weight`).  

- [ ] **1.2 Specify “public API” functions for engine pipelines**  
  - **Goal**: Design the top‑level functions backend will call (even if you don’t implement all of them now).  
  - **Files**: `backend/app/engine/pipelines/__init__.py`.  
  - **What to do**:  
    - Add function **signatures only** (with `pass` or `NotImplementedError` for now) for:  
      - `run_equity_risk_analysis(symbol: str, price_history: pd.DataFrame, positions_row: dict | None) -> dict`  
      - `run_portfolio_risk_analysis(portfolio_id: str, price_history: pd.DataFrame, positions: pd.DataFrame) -> dict`  
      - `run_portfolio_optimization(portfolio_id: str, price_history: pd.DataFrame, positions: pd.DataFrame) -> dict`  
    - Document each function to clarify:  
      - **Inputs**: what the backend will pass (symbols, portfolio IDs, price history, positions).  
      - **Outputs**: a nested dict with sections such as `"metrics"`, `"forecast"`, `"optimization"`, `"diagnostics"`, designed to map nicely to SRS `Risk_Assessment` / `Risk_Metric`.  

---

## Phase 2 — Market Data & Returns Preparation (30–40 min)

- [ ] **2.1 Implement a basic price history fetcher**  
  - **Goal**: Get historical prices for a single symbol so you can compute returns and risk.  
  - **File**: `backend/app/engine/data/market_data.py`.  
  - **What to do**:  
    - In `MarketDataSource.fetch_price_history`, replace `NotImplementedFeatureError` with a real implementation using `yfinance`:  
      - Fetch `Adj Close` prices for a single `symbol` over a configurable `period` and `interval`.  
      - Ensure the returned `pd.DataFrame` is indexed by date and has a single `Adj Close` column or a column named after the symbol.  
    - Add basic validation: raise a clear exception if:  
      - No data is returned.  
      - The index is empty or not datetime.  
    - Add docstring specifying how many rows of data you aim for (e.g. 1 year daily history).  

- [ ] **2.2 Add utilities for computing returns from prices**  
  - **Goal**: Convert price history into log or simple returns, which will be used everywhere else.  
  - **File**: `backend/app/engine/data/portfolio_data.py`.  
  - **What to do**:  
    - Implement helper functions such as:  
      - `compute_log_returns(price_history: pd.DataFrame) -> pd.DataFrame` (e.g. `np.log(price / price.shift(1))`).  
      - `align_prices_to_positions(price_history: pd.DataFrame, positions: pd.DataFrame) -> pd.DataFrame` (subset/reindex columns to symbols in `positions`).  
    - Add docstrings explaining expected shapes and how NaNs at the beginning are handled (e.g. drop first row after differencing).  
    - Keep functions **stateless and pure**. No DB calls here.  

---

## Phase 3 — Core Risk Metrics (40–60 min)

- [ ] **3.1 Implement volatility, exposure, and concentration calculations**  
  - **Goal**: Fulfill FR4 (Risk Assessment) by computing per‑equity and portfolio‑level risk metrics.  
  - **File**: `backend/app/engine/risk/metrics.py`.  
  - **What to do**:  
    - Implement `RiskMetricsEngine.compute_volatility(returns: pd.Series) -> float`:  
      - Use daily returns and compute annualized volatility, e.g. `returns.std() * np.sqrt(252)`.  
      - Handle NaNs by dropping them.  
    - Implement `compute_exposure(positions: pd.DataFrame) -> pd.Series`:  
      - Take positions with columns like `symbol`, `market_value` or `weight`.  
      - Compute percentage weight per symbol (exposure) as `market_value / total_market_value`.  
      - Return a `pd.Series` indexed by symbol.  
    - Implement `compute_concentration(weights: pd.Series) -> float`:  
      - Example: Herfindahl–Hirschman Index \(HHI = \sum w_i^2\).  
      - Optionally map HHI into a `0–100` risk concentration score.  
    - Add docstrings and note assumptions (daily data, 252 trading days, etc.).  

- [ ] **3.2 Design a basic “risk score” computation**  
  - **Goal**: Provide a single numeric `risk_score` that can map to the SRS `Risk_Assessment.risk_score` (0–100).  
  - **File**: `backend/app/engine/risk/metrics.py`.  
  - **What to do**:  
    - Add a method like `compute_risk_score(volatility: float, concentration: float) -> float`.  
    - Define a simple heuristic, for example:  
      - Normalize volatility and concentration into the range \([0, 1]\).  
      - Combine them via weighted sum, then rescale to `0–100`.  
    - Document how these map to `Risk_Metric` concepts (e.g. “Volatility” metric, “Concentration” metric).  

---

## Phase 4 — Volatility Forecasting (30–45 min)

- [ ] **4.1 Implement a simple time‑series volatility forecast**  
  - **Goal**: Provide a future volatility estimate for an equity or portfolio to support “future risk” views.  
  - **File**: `backend/app/engine/forecasting/volatility.py`.  
  - **What to do**:  
    - In `VolatilityForecaster.forecast(self, returns: pd.Series) -> float`:  
      - Start with a simple model due to time constraints, e.g.:  
        - Use rolling window standard deviation over the last N days and annualize.  
        - OR use `ExponentialSmoothing` on absolute returns or squared returns, then convert to an annualized volatility.  
      - Handle edge cases (too few points → raise a clear exception or return `np.nan`).  
      - Document clearly that this is a simple forecast that can be swapped out later for GARCH/ML models.  

- [ ] **4.2 Add helper to compute forecast for multiple symbols**  
  - **Goal**: Allow portfolio‑level forecasting by looping over each symbol.  
  - **File**: `backend/app/engine/forecasting/volatility.py`.  
  - **What to do**:  
    - Add a function (top‑level or method) such as `forecast_panel(price_history: pd.DataFrame) -> pd.Series`:  
      - Compute returns per column (symbol).  
      - Apply `VolatilityForecaster.forecast` per column.  
      - Return a `pd.Series` mapping symbol → forecasted annualized volatility.  

---

## Phase 5 — Portfolio Optimization (40–60 min)

- [ ] **5.1 Implement a basic mean–variance optimizer**  
  - **Goal**: Optimize portfolio weights using historical prices in line with SRS “assist analysts in making risk‑aware decisions”.  
  - **File**: `backend/app/engine/optimization/optimizer.py`.  
  - **What to do**:  
    - In `PortfolioOptimizer.optimize(self, price_history: pd.DataFrame) -> dict[str, float]`:  
      - Use `pypfopt.expected_returns.mean_historical_return` to estimate expected returns.  
      - Use `pypfopt.risk_models.sample_cov` for covariance.  
      - Build an `EfficientFrontier` and compute either **max Sharpe ratio** or **minimum volatility** weights.  
      - Clean weights and return them as a simple dict `{symbol: weight}`.  
      - Add basic validation (e.g. at least 2–3 assets, enough data rows).  

- [ ] **5.2 Expose constraints and options for optimization**  
  - **Goal**: Make it easy for backend/UI to choose optimization style (risk‑averse vs return‑seeking).  
  - **File**: `backend/app/engine/optimization/optimizer.py`.  
  - **What to do**:  
    - Extend `optimize` to accept optional parameters, e.g.:  
      - `method: str = "max_sharpe"` (`"min_vol"`, `"risk_parity"` in the future).  
      - `weight_bounds: tuple[float, float] = (0.0, 1.0)`.  
    - Document behavior for each method (for today, implement only one or two methods).  
    - Return additional diagnostics alongside weights, e.g.:  
      - Expected annual return.  
      - Expected volatility.  
      - Sharpe ratio.  
    - Structure the return as:  
      - `{"weights": {...}, "metrics": {...}}` so it can go straight into a report.  

---

## Phase 6 — Pipelines: Equity‑Level & Portfolio‑Level Flows (45–60 min)

- [ ] **6.1 Implement equity‑level risk analysis pipeline**  
  - **Goal**: Given a single symbol, compute metrics + forecast + risk score.  
  - **File**: `backend/app/engine/pipelines/__init__.py`.  
  - **What to do**:  
    - Implement `run_equity_risk_analysis`:  
      - Inputs: `symbol`, `price_history` for that symbol (or fetch internally using `MarketDataSource` if you prefer).  
      - Steps:  
        1. Compute returns using your Phase 2 helpers.  
        2. Use `RiskMetricsEngine.compute_volatility` for current volatility.  
        3. Use `VolatilityForecaster.forecast` for future volatility.  
        4. Optionally compute a per‑equity exposure (weight within its portfolio row if provided).  
        5. Compute a `risk_score`.  
      - Output:  
        - Dict like:  
          - `{"symbol": ..., "metrics": {"volatility": ..., "current_vol": ..., "forecast_vol": ...}, "risk_score": ..., "raw": {...optional...}}`.  

- [ ] **6.2 Implement portfolio‑level risk analysis pipeline**  
  - **Goal**: Aggregate risk across a portfolio (volatility, exposure, concentration, risk scores).  
  - **File**: `backend/app/engine/pipelines/__init__.py`.  
  - **What to do**:  
    - Implement `run_portfolio_risk_analysis`:  
      - Inputs: `portfolio_id`, `price_history` (multi‑asset), `positions` (symbols + positions).  
      - Steps:  
        1. Align price history to symbols in `positions`.  
        2. Compute returns panel.  
        3. Compute **per‑symbol** volatility using `RiskMetricsEngine`.  
        4. Compute **portfolio weights/exposure** using `compute_exposure`.  
        5. Compute **concentration** metric.  
        6. Optionally compute portfolio‑level volatility (e.g. weights’ covariance formula).  
        7. Compute portfolio‑level `risk_score`.  
      - Output:  
        - A dict with sections like:  
          - `"portfolio_id"`  
          - `"per_equity"`: {symbol → metrics}  
          - `"portfolio"`: {volatility, concentration, risk_score, exposures}  

- [ ] **6.3 Implement portfolio optimization + diagnostics pipeline**  
  - **Goal**: Run optimization and package results for reporting.  
  - **File**: `backend/app/engine/pipelines/__init__.py`.  
  - **What to do**:  
    - Implement `run_portfolio_optimization`:  
      - Inputs: `portfolio_id`, `price_history`, `positions`.  
      - Steps:  
        1. Align `price_history` to current holdings.  
        2. Call `PortfolioOptimizer.optimize`.  
        3. Compare `current_weights` vs `target_weights` and compute suggested trades (e.g. `delta_weight = target - current`).  
      - Output:  
        - Dict such as:  
          - `"portfolio_id"`  
          - `"optimization"`: `{ "current_weights": ..., "target_weights": ..., "expected_return": ..., "expected_volatility": ..., "sharpe": ... }`  
          - `"suggested_changes"`: list/dict of rebalancing suggestions.  

---

## Phase 7 — Reporting‑Friendly Structures (20–30 min)

Even though the backend and frontend will render actual reports, you should structure outputs so they can be turned into **Risk Reports** (FR5) and mapped to `Risk_Assessment` and `Risk_Metric` tables.

- [ ] **7.1 Define a common report schema for engine outputs**  
  - **Goal**: Ensure all pipelines return data structures that are easy for the backend to persist and the frontend to render.  
  - **File**: `backend/app/engine/pipelines/__init__.py`.  
  - **What to do**:  
    - Create standard top‑level keys for all pipeline outputs, for example:  
      - `"metadata"`: portfolio ID, user ID (if available), timestamps, parameters used.  
      - `"metrics"`: flattened metrics ready to map to `Risk_Metric` / `Risk_Assessment`.  
      - `"details"`: nested diagnostic data (per‑symbol metrics, time series).  
      - `"optimization"`: if applicable, optimization results and suggested changes.  
    - Document (via docstrings or comments) **how each field maps** to the SRS schema:  
      - `risk_score` → `Risk_Assessment.risk_score`.  
      - Metric names → `Risk_Metric.metric_name`.  

- [ ] **7.2 Add small helpers to convert engine results → DB‑friendly records (optional, without importing ORM)**  
  - **Goal**: Make a thin mapping layer that backend services can reuse.  
  - **File**: `backend/app/engine/pipelines/__init__.py` (or a new `backend/app/engine/pipelines/mappers.py` if you prefer).  
  - **What to do**:  
    - Implement pure functions that accept the dicts from your pipelines and yield:  
      - A list of metric dicts like `{"metric_name": ..., "description": ..., "threshold_value": ..., "category": ...}`.  
      - A list of risk assessment dicts like `{"equity_id": ..., "metric_id": ..., "analyst_id": ..., "risk_score": ..., "assessment_date": ..., "remarks": ...}`.  
    - These should not know about actual ORM models—just return plain dicts.  

---

## Phase 8 — Validation, Testing & Performance (30–45 min)

- [ ] **8.1 Create simple unit tests for core analytics**  
  - **Goal**: Verify that key computations behave as expected and avoid regressions.  
  - **Files**:  
    - `backend/tests/test_placeholder.py` (replace with real tests or create new test files like `test_risk_metrics.py`, `test_optimizer.py`).  
  - **What to do**:  
    - Write tests for:  
      - `compute_volatility` with known synthetic return series.  
      - `compute_exposure` and `compute_concentration` on small example portfolios.  
      - `PortfolioOptimizer.optimize` with a tiny price matrix to ensure weights sum to 1 and are non‑negative (if that’s the constraint).  
      - `VolatilityForecaster.forecast` returns a finite positive float for a reasonable series.  

- [ ] **8.2 Add basic performance checks / considerations**  
  - **Goal**: Respect NFR2 (risk analysis within ~3 seconds for standard datasets).  
  - **Files**: same as above, plus any performance‑critical helpers.  
  - **What to do**:  
    - For now, add comments/docstrings about expected dataset sizes (e.g. portfolios up to N symbols, M days).  
    - Use vectorized NumPy/pandas operations where possible (you likely already will by design).  
    - Optionally time a few calls locally to see if they’re comfortably under 3 seconds.  

---

## Phase 9 — Documentation for Backend Integration (15–20 min)

- [ ] **9.1 Document engine usage examples for backend devs**  
  - **Goal**: Make it trivial for someone else to call your engine from FastAPI services.  
  - **Files**:  
    - `engine_specs.md` (this file)  
    - Optionally `backend/app/engine/__init__.py` for short usage examples in docstrings.  
  - **What to do**:  
    - Add short, language‑agnostic examples such as:  
      - “Given a `PriceHistory` DataFrame and `positions` DataFrame, call `run_portfolio_risk_analysis` to get a dict the API can return.”  
      - “Use `run_portfolio_optimization` to produce target weights and diagnostics for the report endpoint.”  
    - Explicitly list which functions are meant to be called from:  
      - `risk_service.py`  
      - `portfolio_service.py`  
      - `report_service.py`  

---

## Phase 10 — Stretch Ideas (if Time Remains)

These are nice‑to‑have enhancements if you finish early.

- [ ] **10.1 Add alternative risk models**  
  - **Goal**: Support additional metrics beyond simple volatility (e.g. downside risk, Value‑at‑Risk).  
  - **File**: `backend/app/engine/risk/metrics.py`.  
  - **What to do**:  
    - Implement functions like `compute_var` (historical VaR) or `compute_cvar`.  
    - Integrate them into risk scores and report structures.  

- [ ] **10.2 Improve forecasting models**  
  - **Goal**: Replace simple volatility forecasting with GARCH or ML methods.  
  - **File**: `backend/app/engine/forecasting/volatility.py`.  
  - **What to do**:  
    - Add optional models (e.g. `arch` package GARCH) and a flag to choose model type.  

- [ ] **10.3 Add alert logic stubs using monitoring module**  
  - **Goal**: Prepare for automated alerts when risk breaches thresholds (in line with SRS “timely reports”).  
  - **File**: `backend/app/engine/monitoring/alerts.py`.  
  - **What to do**:  
    - Define functions that accept current/forecasted risk metrics plus thresholds, and output alert dicts (no actual notification sending).  
    - Ensure thresholds can map to `Risk_Metric.threshold_value`.  

---

## How to Use This Roadmap in 4 Hours

1. **First 30–45 min**: Phases 0–2 (interfaces, data, returns).  
2. **Next 60–90 min**: Phases 3–6 (metrics, forecasting, optimization, pipelines) — this is the core analytics.  
3. **Last 60 min**: Phases 7–9 (report‑friendly structures, basic tests, documentation).  
4. **Only if time remains**: Phase 10 stretch items.  

As you implement, keep each function **small, testable, and pure**, and ensure all outputs are easily serializable so the backend can store them in the relational schema described in the SRS.

