# Loopline

Loopline is a unified professional social network and work marketplace built around one account, one profile, and multiple work contexts. A person can publish opportunities, apply for work, communicate, complete projects, build reputation, and return to the feed without switching roles or dashboards.

## Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, React Router, ESLint
- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy
- **Database:** Persistent SQLite
- **Auth:** Gmail-only email registration, development OTP, secure password hashing, signed sessions
- **Payments:** Internal demo wallet only. No gateways or real money.

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API starts with empty business tables. In development mode, OTP values are returned in the registration response and logged to the server console; configure SMTP in `.env` to deliver them by email.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://localhost:8000`. Open the URL printed by Vite.

## Product rules implemented

- All accounts use the same user model; requester and assignee are work contexts.
- Registration and password reset only accept `@gmail.com` addresses.
- OTP records expire and have an attempt limit. SMTP is optional; development OTP is safe to demo.
- Work deadlines are calculated server-side from `accepted_at`.
- Expired active work becomes overdue without deleting or reassigning it.
- Revision and resubmission are explicit work-state transitions.
- Completion debits and credits demo wallets atomically.
- Every important side effect creates backend notifications.
- The AI assistant routes people, opportunity, deadline, and general requests to database-backed actions. It never performs irreversible actions automatically.

## Useful commands

```bash
# frontend
npm run lint
npm run build

# backend
pytest
```

The SQLite file is created at `database/app.db`. Copy `.env.example` to `.env` to customize it. The application starts with empty business tables; every profile, post, opportunity, application, message, notification, wallet entry, and review is created from real user actions.