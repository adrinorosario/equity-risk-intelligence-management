INSERT INTO users (
        name,
        email,
        role,
        password_hash,
        created_at,
        status
    )
VALUES (
        'Alice Analyst',
        'alice@erims.com',
        'Analyst',
        '$2b$12$iWCOy4HggNHSDwycI0.qcOmacYJOS4TEr6k7p0/uX9J0qrpLDcvy2',
        '2026-03-04',
        'Active'
    ),
    (
        'Bob Manager',
        'bob@erims.com',
        'Manager',
        '$2b$12$iWCOy4HggNHSDwycI0.qcOmacYJOS4TEr6k7p0/uX9J0qrpLDcvy2',
        '2026-03-04',
        'Active'
    ),
    (
        'Charlie Investor',
        'charlie@erims.com',
        'Investor',
        '$2b$12$Rk8kc0pCs5qeU/lKyDXMxOshjBklCkvm9KxawSaWVTXApFXe8njgq',
        '2026-03-04',
        'Active'
    );
INSERT INTO portfolio (
        user_id,
        portfolio_name,
        creation_date,
        description
    )
VALUES (
        1,
        'Growth Fund A',
        '2026-03-04',
        'Aggressive growth tech focus'
    ),
    (
        1,
        'Value Fund B',
        '2026-03-04',
        'Stable dividend paying stocks'
    ),
    (
        3,
        'Charlie Tech',
        '2026-03-04',
        'Personal tech holdings'
    ),
    (
        3,
        'Charlie Healthcare',
        '2026-03-04',
        'Healthcare and Biotech'
    );
-- Growth Fund A (portfolio_id=3)
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
VALUES (
        3,
        'NVIDIA',
        'Technology',
        250000,
        'NASDAQ',
        '2024-01-10'
    ),
    (
        3,
        'Alphabet Inc.',
        'Technology',
        180000,
        'NASDAQ',
        '2023-11-05'
    ),
    (
        3,
        'Meta Platforms',
        'Technology',
        120000,
        'NASDAQ',
        '2024-02-01'
    );
-- Value Fund B (portfolio_id=4)
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
VALUES (
        4,
        'Johnson & Johnson',
        'Healthcare',
        80000,
        'NYSE',
        '2022-05-15'
    ),
    (
        4,
        'Procter & Gamble',
        'Consumer Goods',
        75000,
        'NYSE',
        '2022-08-20'
    ),
    (
        4,
        'Coca-Cola',
        'Consumer Goods',
        60000,
        'NYSE',
        '2023-01-10'
    );
-- Charlie Tech (portfolio_id=5)
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
VALUES (
        5,
        'Tesla',
        'Automotive',
        45000,
        'NASDAQ',
        '2024-01-15'
    ),
    (
        5,
        'Advanced Micro Devices',
        'Technology',
        90000,
        'NASDAQ',
        '2024-02-15'
    );
-- Charlie Healthcare (portfolio_id=6)
INSERT INTO equity (
        portfolio_id,
        company_name,
        sector,
        market_value,
        exchange,
        purchase_date
    )
VALUES (
        6,
        'UnitedHealth Group',
        'Healthcare',
        110000,
        'NYSE',
        '2023-10-01'
    ),
    (
        6,
        'Pfizer',
        'Healthcare',
        50000,
        'NYSE',
        '2023-11-20'
    );
-- Risk Assessments
INSERT INTO risk_assessment (
        equity_id,
        metric_id,
        analyst_id,
        risk_score,
        assessment_date,
        remarks
    )
VALUES (
        3,
        1,
        1,
        85,
        '2026-03-04',
        'High volatility expected next quarter'
    ),
    (
        4,
        1,
        1,
        45,
        '2026-03-04',
        'Stable regulatory environment'
    ),
    (
        5,
        1,
        1,
        75,
        '2026-03-04',
        'Ad spend variability'
    ),
    (
        6,
        1,
        1,
        25,
        '2026-03-04',
        'Defensive stock, low volatility'
    ),
    (
        7,
        1,
        1,
        30,
        '2026-03-04',
        'Strong consumer base, low risk'
    ),
    (
        8,
        1,
        1,
        28,
        '2026-03-04',
        'Steady dividend aristocrat'
    ),
    (
        9,
        1,
        1,
        90,
        '2026-03-04',
        'Highly volatile based on EV market sentiment'
    ),
    (
        10,
        1,
        1,
        80,
        '2026-03-04',
        'Semiconductor cycle dependency'
    ),
    (
        11,
        1,
        1,
        40,
        '2026-03-04',
        'Industry leader, stable premiums'
    ),
    (
        12,
        1,
        1,
        50,
        '2026-03-04',
        'Pipeline execution risks'
    );