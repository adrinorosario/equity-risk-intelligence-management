-- TLDR; Initial relational schema based on SRS.pdf.
-- TODO: Replace INT PKs with generated IDs, add indexes, and migrate to Alembic-managed migrations.

CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  role VARCHAR(20) DEFAULT 'Investor',
  password_hash VARCHAR(200) NOT NULL,
  created_at DATE DEFAULT CURRENT_DATE,
  status VARCHAR(20) DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS portfolio (
  portfolio_id INT PRIMARY KEY,
  user_id INT NOT NULL,
  portfolio_name VARCHAR(100) NOT NULL,
  creation_date DATE,
  total_value DECIMAL(15,2) CHECK (total_value >= 0),
  risk_level VARCHAR(20),
  description VARCHAR(200),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS equity (
  equity_id INT PRIMARY KEY,
  portfolio_id INT NOT NULL,
  company_name VARCHAR(150) NOT NULL,
  sector VARCHAR(100),
  market_value DECIMAL(15,2) CHECK (market_value >= 0),
  exchange VARCHAR(50),
  purchase_date DATE,
  FOREIGN KEY (portfolio_id) REFERENCES portfolio(portfolio_id)
);

CREATE TABLE IF NOT EXISTS risk_metric (
  metric_id INT PRIMARY KEY,
  metric_name VARCHAR(100) NOT NULL,
  description VARCHAR(200),
  threshold_value DECIMAL(6,2),
  category VARCHAR(50),
  created_at DATE DEFAULT CURRENT_DATE,
  status VARCHAR(20) DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS risk_assessment (
  assessment_id INT PRIMARY KEY,
  equity_id INT NOT NULL,
  metric_id INT NOT NULL,
  analyst_id INT NOT NULL,
  risk_score DECIMAL(6,2) CHECK (risk_score BETWEEN 0 AND 100),
  assessment_date DATE,
  remarks VARCHAR(200),
  FOREIGN KEY (equity_id) REFERENCES equity(equity_id),
  FOREIGN KEY (metric_id) REFERENCES risk_metric(metric_id),
  FOREIGN KEY (analyst_id) REFERENCES users(user_id)
);
