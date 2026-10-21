# Local AI Data Analyst

**Ask questions in plain English. Get answers from your local database.**

A lightweight, local-first SQL analytics agent built with **Python · LangGraph · Ollama · PostgreSQL**.   
It uses **Qwen3.5:9b** to inspect database schemas, generate SQL, run read-only queries, and explain results—without an external LLM API.  

> **Status:** Local prototype. Tested with the Titanic dataset; not production-ready.

## Prerequisites

- Windows, ideally **16 GB RAM or more** for this model configuration
- Python 3.11+ and Git
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running)
- [Ollama](https://ollama.com/download)

## Quick start

Run these commands in **PowerShell**, from the repository root unless noted.

### 1. Get the code and prepare Python

```powershell
# Skip the clone step if you already have the project locally.
git clone https://github.com/Tais19991/local-ai-data-analyst.git
cd local-ai-data-analyst

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Download and check the local model

Install Ollama from the link above, then run:

```powershell
ollama pull qwen3.5:9b
ollama list
```

Optional interactive test: `ollama run qwen3.5:9b` (exit with `/bye`). Ollama normally serves its local API at `http://localhost:11434`.

### 3. Start PostgreSQL and load Titanic data

```powershell
docker compose up -d
docker compose ps
python database/load_titanic.py
```

Expected loader output: `Loaded 891 passengers`.

> The SQL scripts in `database/sql/` are applied automatically **only when the PostgreSQL data volume is first initialized**. The loader requires an internet connection to fetch the sample CSV unless you've cached it locally.

### 4. Create a read-only database account

Open PostgreSQL:

```powershell
docker exec -it local-ai-postgres psql -U analyst -d titanic_db
```

At the `titanic_db=#` prompt, run the following SQL (including the semicolons):

```sql
CREATE ROLE ai_reader LOGIN PASSWORD 'local_reader_password';
GRANT CONNECT ON DATABASE titanic_db TO ai_reader;
GRANT USAGE ON SCHEMA titanic TO ai_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA titanic TO ai_reader;

ALTER DEFAULT PRIVILEGES FOR ROLE analyst IN SCHEMA titanic
GRANT SELECT ON TABLES TO ai_reader;
```

Type `\q` to exit `psql`. If the role already exists, skip the `CREATE ROLE` statement.

### 5. Configure the agent

Create `.env` in the repository root (or copy `.env.example` if available):

```dotenv
OLLAMA_MODEL=qwen3.5:9b
OLLAMA_BASE_URL=http://localhost:11434
DATABASE_URL=postgresql+psycopg://ai_reader:local_reader_password@localhost:5432/titanic_db
```

The database URL must match the credentials and port in your `docker-compose.yml`. **Never commit `.env` to Git.** The credentials above are for local development only.

### 6. Verify the connection and run the agent

```powershell
python database/test_connection.py
python -m database.test_tools
python -m agent.cli
```

Try :

> What was the survival rate by passenger class?

For the standard 891-passenger Titanic dataset, expected results are:

| Passenger class | Survival rate |
| --- | ---: |
| First | 62.96% |
| Second | 47.28% |
| Third | 24.24% |

You can also ask: *What was the average age of passengers who survived?*

## Project layout

```text
agent/               # Database access, tools, LangGraph agent, CLI
database/sql/        # PostgreSQL initialization scripts
database/load_titanic.py
database/test_connection.py
database/test_tools.py
docker-compose.yml
requirements.txt
.env.example         # Optional, safe-to-commit configuration template
```

## Troubleshooting

| Problem | Check |
| --- | --- |
| `ModuleNotFoundError` | Activate `.venv`, then run `python -m pip install -r requirements.txt` |
| Database connection refused | Run `docker compose ps`; check PostgreSQL port and `.env` |
| Model unavailable | Run `ollama list`; confirm `OLLAMA_MODEL` |
| `titanic_db-#` prompt in `psql` | Finish the SQL statement with `;`, or press `Ctrl+C` to cancel |
| Tables missing | Initialization SQL only runs on a fresh PostgreSQL data volume; inspect `database/sql/` and Docker logs |

## Security and limitations

This is a **development prototype**, not a secure SQL sandbox. The agent should connect with the **read-only `ai_reader` role**. A basic `SELECT` prefix check is not sufficient SQL validation; robust query parsing, timeouts, resource limits, access controls, and tests are needed before using sensitive or production data. Current query results are capped at 100 rows in `agent/db.py`.

**Next:** Add SQL execution tracing, stronger query safeguards, and conversational memory.
