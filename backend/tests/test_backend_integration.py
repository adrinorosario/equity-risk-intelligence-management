"""
ERIMS Backend Integration Tests
================================

Five tests that verify the core backend flows end-to-end through the
FastAPI HTTP layer, using the in-memory SQLite test database.

Tests covered:
1. User registration (POST /api/v1/auth/register)
2. User login + JWT token (POST /api/v1/auth/login)
3. Create portfolio (POST /api/v1/portfolios/)
4. Add equity to portfolio + list equities (POST + GET)
5. Full flow: register → login → create portfolio → add equity → verify ownership
"""

import pytest
from httpx import AsyncClient


# ---------------------------------------------------------------------------
# 1. Registration creates a new user and returns their public profile
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """POST /api/v1/auth/register should create a user and return UserPublic."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Alice Analyst",
            "email": "alice@erimstest.com",
            "password": "Str0ngP@ss!",
            "role": "Analyst",
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Alice Analyst"
    assert data["email"] == "alice@erimstest.com"
    assert data["role"] == "Analyst"
    assert "user_id" in data
    # Password hash must never be exposed
    assert "password_hash" not in data
    assert "password" not in data


# ---------------------------------------------------------------------------
# 2. Login returns a valid JWT bearer token
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_login_returns_token(client: AsyncClient):
    """POST /api/v1/auth/login should return an access_token after registration."""
    # First, register
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Bob Broker",
            "email": "bob@erimstest.com",
            "password": "S3cur3Pass!",
            "role": "Investor",
        },
    )

    # Now login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "bob@erimstest.com",
            "password": "S3cur3Pass!",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20  # JWT tokens are lengthy


# ---------------------------------------------------------------------------
# 3. Authenticated user can create a portfolio
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_portfolio(client: AsyncClient):
    """POST /api/v1/portfolios/ should create a portfolio for the logged-in user."""
    # Register + login
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Carol Capital",
            "email": "carol@erimstest.com",
            "password": "MyP@ssw0rd!",
            "role": "Investor",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "carol@erimstest.com", "password": "MyP@ssw0rd!"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create portfolio
    response = await client.post(
        "/api/v1/portfolios/",
        json={
            "user_id": 0,  # will be overridden by the server to the auth'd user
            "portfolio_name": "Growth Fund",
            "description": "High-growth tech equities",
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["portfolio_name"] == "Growth Fund"
    assert data["description"] == "High-growth tech equities"
    assert "portfolio_id" in data


# ---------------------------------------------------------------------------
# 4. Add equity to a portfolio, then list equities
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_add_and_list_equities(client: AsyncClient):
    """POST + GET equities within a portfolio should round-trip correctly."""
    # Setup: register, login, create portfolio
    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Dave Dealer",
            "email": "dave@erimstest.com",
            "password": "D@veP@ss1!",
            "role": "Investor",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "dave@erimstest.com", "password": "D@veP@ss1!"},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    portfolio_resp = await client.post(
        "/api/v1/portfolios/",
        json={"user_id": 0, "portfolio_name": "Tech Leaders"},
        headers=headers,
    )
    portfolio_id = portfolio_resp.json()["portfolio_id"]

    # Add two equities
    eq1 = await client.post(
        f"/api/v1/portfolios/{portfolio_id}/equities",
        json={
            "portfolio_id": portfolio_id,
            "company_name": "Apple Inc.",
            "sector": "Technology",
            "market_value": 150000.00,
            "exchange": "NASDAQ",
        },
        headers=headers,
    )
    assert eq1.status_code == 201, eq1.text

    eq2 = await client.post(
        f"/api/v1/portfolios/{portfolio_id}/equities",
        json={
            "portfolio_id": portfolio_id,
            "company_name": "Microsoft Corp.",
            "sector": "Technology",
            "market_value": 200000.00,
            "exchange": "NASDAQ",
        },
        headers=headers,
    )
    assert eq2.status_code == 201, eq2.text

    # List equities
    list_resp = await client.get(
        f"/api/v1/portfolios/{portfolio_id}/equities",
        headers=headers,
    )
    assert list_resp.status_code == 200, list_resp.text
    equities = list_resp.json()
    assert len(equities) == 2
    names = {e["company_name"] for e in equities}
    assert names == {"Apple Inc.", "Microsoft Corp."}


# ---------------------------------------------------------------------------
# 5. Full end-to-end: register → login → portfolio → equity → verify /me
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_full_user_flow(client: AsyncClient):
    """End-to-end smoke test: register, login, /me, portfolio, equity."""
    # 1. Register
    reg = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Eve Equity",
            "email": "eve@erimstest.com",
            "password": "Ev3P@ssw0rd!",
            "role": "Analyst",
        },
    )
    assert reg.status_code == 201
    user_id = reg.json()["user_id"]

    # 2. Login
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "eve@erimstest.com", "password": "Ev3P@ssw0rd!"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. GET /users/me – verify identity
    me = await client.get("/api/v1/users/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "eve@erimstest.com"
    assert me.json()["role"] == "Analyst"

    # 4. Create portfolio
    pf = await client.post(
        "/api/v1/portfolios/",
        json={"user_id": 0, "portfolio_name": "Value Fund"},
        headers=headers,
    )
    assert pf.status_code == 201
    pf_id = pf.json()["portfolio_id"]
    # Server must enforce ownership to the authenticated user
    assert pf.json()["user_id"] == user_id

    # 5. Add equity
    eq = await client.post(
        f"/api/v1/portfolios/{pf_id}/equities",
        json={
            "portfolio_id": pf_id,
            "company_name": "Google LLC",
            "sector": "Technology",
            "market_value": 300000.00,
        },
        headers=headers,
    )
    assert eq.status_code == 201
    assert eq.json()["company_name"] == "Google LLC"

    # 6. List portfolios – must contain the one we just created
    pfs = await client.get("/api/v1/portfolios/", headers=headers)
    assert pfs.status_code == 200
    assert any(p["portfolio_name"] == "Value Fund" for p in pfs.json())
