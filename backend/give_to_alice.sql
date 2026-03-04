UPDATE portfolio
SET user_id = (
        SELECT user_id
        FROM users
        WHERE email = 'alice@erims.com'
    );
UPDATE risk_assessment
SET analyst_id = (
        SELECT user_id
        FROM users
        WHERE email = 'alice@erims.com'
    );