# Local AI Data Analyst — initial agent package

This is the first implementation increment. It requires an Ollama server and an existing PostgreSQL database; Docker and synthetic seed data are not yet included.

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
Copy-Item .env.example .env
ollama pull qwen3:4b
.\.venv\Scripts\python.exe -m agent.cli
```

Configure `DATABASE_URL` in `.env` before running. Use a PostgreSQL account with **SELECT-only permissions**. The default credentials are placeholders for a future local test database, not production credentials.

Run tests with `.\.venv\Scripts\python.exe -m pytest`.

## Security limitations

This is a prototype, not a hardened SQL sandbox. The validator blocks common write operations and disallows unapproved SQL functions, but a dedicated read-only database role, schema allowlisting at the database layer, network restrictions, and integration tests are mandatory before connecting sensitive data. Query results may be truncated to `MAX_QUERY_ROWS`.
