# Loopline backend

FastAPI + SQLAlchemy backend with a persistent SQLite database. The backend starts empty and only stores records created through the application.

```bash
uvicorn app.main:app --reload --port 8000
```

The app uses an internal signed session token, Gmail-only validation, development OTPs when SMTP is not configured, server-side deadline calculations, revision workflows, and an atomic simulated wallet. No real payment provider is used.