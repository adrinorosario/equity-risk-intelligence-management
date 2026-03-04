-- New Portfolios for Test User (user_id = 2)
INSERT INTO portfolio (
        user_id,
        portfolio_name,
        creation_date,
        description
    )
VALUES (
        2,
        'Tech Giants Vanguard',
        '2026-03-04',
        'Mega cap technology stocks'
    ),
    (
        2,
        'Renewable Energy Focus',
        '2026-03-04',
        'Sustainable and green energy holdings'
    );
-- New Portfolios for Adrino (user_id = 1)
INSERT INTO portfolio (
        user_id,
        portfolio_name,
        creation_date,
        description
    )
VALUES (
        1,
        'Global Financials',
        '2026-03-04',
        'Major banks and payment processors'
    ),
    (
        1,
        'Emerging Markets ETF Mix',
        '2026-03-04',
        'High growth international equities'
    );
-- Let's get the inserted portfolio IDs. Assuming auto-increment, they will likely be 7, 8, 9, 10
-- We will just insert equities with explicit sub-selects to be failsafe.
-- Equities for Tech Giants Vanguard
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Amazon.com Inc.',
    'Consumer Discretionary',
    310000,
    'NASDAQ',
    '2023-08-15'
FROM portfolio
WHERE portfolio_name = 'Tech Giants Vanguard'
    AND user_id = 2;
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Alphabet Inc.',
    'Technology',
    280000,
    'NASDAQ',
    '2023-09-01'
FROM portfolio
WHERE portfolio_name = 'Tech Giants Vanguard'
    AND user_id = 2;
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Meta Platforms',
    'Technology',
    210000,
    'NASDAQ',
    '2024-01-20'
FROM portfolio
WHERE portfolio_name = 'Tech Giants Vanguard'
    AND user_id = 2;
-- Equities for Renewable Energy Focus
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'NextEra Energy',
    'Utilities',
    85000,
    'NYSE',
    '2022-11-10'
FROM portfolio
WHERE portfolio_name = 'Renewable Energy Focus'
    AND user_id = 2;
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'First Solar',
    'Energy',
    60000,
    'NASDAQ',
    '2023-04-12'
FROM portfolio
WHERE portfolio_name = 'Renewable Energy Focus'
    AND user_id = 2;
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Enphase Energy',
    'Technology',
    45000,
    'NASDAQ',
    '2023-05-22'
FROM portfolio
WHERE portfolio_name = 'Renewable Energy Focus'
    AND user_id = 2;
-- Equities for Global Financials
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'JPMorgan Chase & Co.',
    'Financials',
    150000,
    'NYSE',
    '2021-03-10'
FROM portfolio
WHERE portfolio_name = 'Global Financials'
    AND user_id = 1;
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Visa Inc.',
    'Financials',
    200000,
    'NYSE',
    '2022-02-18'
FROM portfolio
WHERE portfolio_name = 'Global Financials'
    AND user_id = 1;
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Goldman Sachs',
    'Financials',
    120000,
    'NYSE',
    '2023-07-30'
FROM portfolio
WHERE portfolio_name = 'Global Financials'
    AND user_id = 1;
-- Equities for Emerging Markets
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Alibaba Group',
    'Consumer Discretionary',
    90000,
    'NYSE',
    '2023-10-15'
FROM portfolio
WHERE portfolio_name = 'Emerging Markets ETF Mix'
    AND user_id = 1;
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
SELECT portfolio_id,
    'Taiwan Semiconductor',
    'Technology',
    160000,
    'NYSE',
    '2024-01-05'
FROM portfolio
WHERE portfolio_name = 'Emerging Markets ETF Mix'
    AND user_id = 1;
-- Risk Assessments for these new equities. 
-- Assuming metric_id 1 (Volatility) and analyst_id 3 (Alice Analyst)
INSERT INTO risk_assessment (
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
    40,
    '2026-03-04',
    'Steady mega cap'
FROM equity
WHERE company_name = 'Amazon.com Inc.';
INSERT INTO risk_assessment (
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
    35,
    '2026-03-04',
    'Market anchor, stable growth'
FROM equity
WHERE company_name = 'Alphabet Inc.';
INSERT INTO risk_assessment (
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
    65,
    '2026-03-04',
    'Moderate policy risk'
FROM equity
WHERE company_name = 'NextEra Energy';
INSERT INTO risk_assessment (
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
    85,
    '2026-03-04',
    'Highly dependent on subsidies'
FROM equity
WHERE company_name = 'First Solar';
INSERT INTO risk_assessment (
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
    30,
    '2026-03-04',
    'Extremely resilient balance sheet'
FROM equity
WHERE company_name = 'JPMorgan Chase & Co.';
INSERT INTO risk_assessment (
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
    25,
    '2026-03-04',
    'Global duopoly'
FROM equity
WHERE company_name = 'Visa Inc.';
INSERT INTO risk_assessment (
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
    'High geopolitical risk exposure'
FROM equity
WHERE company_name = 'Alibaba Group';
INSERT INTO risk_assessment (
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
    60,
    '2026-03-04',
    'Supply chain concentration risk'
FROM equity
WHERE company_name = 'Taiwan Semiconductor';