-- Add a new Analyst
INSERT OR IGNORE INTO users (
        name,
        email,
        role,
        password_hash,
        created_at,
        status
    )
VALUES (
        'Diana Data',
        'diana@erims.com',
        'Analyst',
        '$2b$12$Rk8kc0pCs5qeU/lKyDXMxOshjBklCkvm9KxawSaWVTXApFXe8njgq',
        '2026-03-04',
        'Active'
    ),
    (
        'Eve Executive',
        'eve@erims.com',
        'Manager',
        '$2b$12$Rk8kc0pCs5qeU/lKyDXMxOshjBklCkvm9KxawSaWVTXApFXe8njgq',
        '2026-03-04',
        'Active'
    );
-- Add new Portfolios for Test User (user_id = 2)
INSERT OR IGNORE INTO portfolio (
        user_id,
        portfolio_name,
        creation_date,
        description
    )
VALUES (
        2,
        'Dividend Kings',
        '2026-03-04',
        'Stocks with 50+ years of dividend increases'
    ),
    (
        2,
        'Asian Markets Growth',
        '2026-03-04',
        'High potential equities in Asia Pacific region'
    );
-- Add new Portfolios for Adrino (user_id = 1)
INSERT OR IGNORE INTO portfolio (
        user_id,
        portfolio_name,
        creation_date,
        description
    )
VALUES (
        1,
        'European Blue Chips',
        '2026-03-04',
        'Stable large-cap European companies'
    ),
    (
        1,
        'Crypto Miners & Tech',
        '2026-03-04',
        'Blockchain related public companies'
    );
-- Equities for Dividend Kings
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    '3M Company',
    'Industrials',
    45000,
    'NYSE',
    '2023-01-15'
FROM portfolio
WHERE portfolio_name = 'Dividend Kings'
    AND user_id = 2;
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Target Corporation',
    'Consumer Discretionary',
    55000,
    'NYSE',
    '2022-11-20'
FROM portfolio
WHERE portfolio_name = 'Dividend Kings'
    AND user_id = 2;
-- Equities for Asian Markets Growth
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Tencent Holdings',
    'Technology',
    120000,
    'HKG',
    '2024-02-10'
FROM portfolio
WHERE portfolio_name = 'Asian Markets Growth'
    AND user_id = 2;
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Toyota Motor',
    'Automotive',
    95000,
    'TYO',
    '2023-09-05'
FROM portfolio
WHERE portfolio_name = 'Asian Markets Growth'
    AND user_id = 2;
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Samsung Electronics',
    'Technology',
    150000,
    'KRX',
    '2024-01-25'
FROM portfolio
WHERE portfolio_name = 'Asian Markets Growth'
    AND user_id = 2;
-- Equities for European Blue Chips
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'LVMH',
    'Consumer Discretionary',
    250000,
    'EPA',
    '2022-06-15'
FROM portfolio
WHERE portfolio_name = 'European Blue Chips'
    AND user_id = 1;
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'ASML Holding',
    'Technology',
    300000,
    'AMS',
    '2023-03-20'
FROM portfolio
WHERE portfolio_name = 'European Blue Chips'
    AND user_id = 1;
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Novartis',
    'Healthcare',
    180000,
    'SWX',
    '2023-08-10'
FROM portfolio
WHERE portfolio_name = 'European Blue Chips'
    AND user_id = 1;
-- Equities for Crypto Miners & Tech
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'MicroStrategy Incorporated',
    'Technology',
    400000,
    'NASDAQ',
    '2024-02-01'
FROM portfolio
WHERE portfolio_name = 'Crypto Miners & Tech'
    AND user_id = 1;
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Coinbase Global',
    'Financials',
    210000,
    'NASDAQ',
    '2024-01-15'
FROM portfolio
WHERE portfolio_name = 'Crypto Miners & Tech'
    AND user_id = 1;
INSERT OR IGNORE INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Marathon Digital',
    'Technology',
    85000,
    'NASDAQ',
    '2024-03-01'
FROM portfolio
WHERE portfolio_name = 'Crypto Miners & Tech'
    AND user_id = 1;
-- Add new Risk Metrics
INSERT OR IGNORE INTO risk_metric (
        metric_name,
        description,
        threshold_value,
        category,
        created_at,
        status
    )
VALUES (
        'Beta',
        'Measure of stock volatility in relation to the overall market',
        1.5,
        'Market Risk',
        '2026-03-04',
        'Active'
    ),
    (
        'VaR (Value at Risk)',
        'Estimate of the maximum potential loss over a timeframe',
        5,
        'Market Risk',
        '2026-03-04',
        'Active'
    ),
    (
        'ESG Risk Score',
        'Environmental, Social, and Governance risk exposure',
        30,
        'Operational Risk',
        '2026-03-04',
        'Active'
    );
-- Add Risk Assessments (Assume metric_id 4 is Beta, 5 is VaR, 6 is ESG) for new equities
-- Let's use analyst_id 6 (Diana Data) if we can look it up, or just hardcode if we know. 
-- Wait, the new analyst Diana Data will probably have user_id 6. We will just use analyst_id 3 (Alice) to be safe.
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    4,
    3,
    85,
    '2026-03-04',
    'Beta of 1.2, slightly higher than market'
FROM equity
WHERE company_name = 'Tencent Holdings';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    5,
    3,
    8,
    '2026-03-04',
    'VaR is 8%, high risk of tail events'
FROM equity
WHERE company_name = 'Tencent Holdings';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    6,
    3,
    45,
    '2026-03-04',
    'Regulatory ESG risks in region'
FROM equity
WHERE company_name = 'Tencent Holdings';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    4,
    3,
    80,
    '2026-03-04',
    'Beta of 0.8, defensive'
FROM equity
WHERE company_name = 'Toyota Motor';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    4,
    3,
    98,
    '2026-03-04',
    'Extreme beta of 3.5 correlated to Bitcoin'
FROM equity
WHERE company_name = 'MicroStrategy Incorporated';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    5,
    3,
    25,
    '2026-03-04',
    'High 25% VaR due to crypto exposure'
FROM equity
WHERE company_name = 'MicroStrategy Incorporated';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    1,
    3,
    95,
    '2026-03-04',
    'Extreme volatility'
FROM equity
WHERE company_name = 'Marathon Digital';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    4,
    3,
    90,
    '2026-03-04',
    'Beta of 1.4'
FROM equity
WHERE company_name = 'ASML Holding';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    6,
    3,
    15,
    '2026-03-04',
    'Excellent ESG rating, low risk'
FROM equity
WHERE company_name = 'ASML Holding';
INSERT OR IGNORE INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
SELECT equity_id,
    6,
    3,
    20,
    '2026-03-04',
    'Strong ESG practices'
FROM equity
WHERE company_name = 'LVMH';