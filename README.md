# Office Device Rental Portal

A web application that allows Legal and General staff to borrow general office equipment such headsets, keyboards, mice, webcams and more. Renting these items requires no approvals and with a click of a button they can rent it out for the day. Staff or guests can log in, pick what they need from the catalogue and confirm a suitable return date. Admins have the ability to manage the catalog and keep an eye on what's out and what's overdue.

## Quick Start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
# 1. Create virtual environment and install dependencies
uv sync

# 2. Seed the database with sample data
uv run python seed.py

# 3. Start the development server
uv run python run.py
```

The app runs at **http://localhost:5001**

------------------------------------------------------------------------------------

## Test Accounts

Populated automatically by `seed.py`:

| Username | Password | Role | Notes |
|---|---|---|---|
| `admin` | `Admin@12345` | Administrator | Full access |
| `alice.jones` | `Pass@Alice1` | Employee | Has active rentals on the dashboard |
| `dave.brown` | `Pass@Dave1` | Employee | **Deactivated account** for testing |

------------------------------------------------------------------------------------

## Running Tests

The test suite covers authentication, role-based access control, SQL injection, XSS, security headers, account lockout, CRUD operations, and password policy which included 46 tests in total.

```bash
# Run all tests
uv run pytest

# Run a specific group
uv run pytest -k TestAccessControl
uv run pytest -k TestSQLInjection
uv run pytest -k TestSecurityHeaders
```
------------------------------------------------------------------------------------