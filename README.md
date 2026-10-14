# Local AI Data Analyst

A lightweight, fully local AI-powered data analytics agent built with **Python, LangGraph, Ollama, and PostgreSQL**.

The project aims to develop an autonomous analytical assistant capable of understanding natural-language requests, exploring database schemas, generating and executing SQL queries, analyzing results, and providing meaningful insights.

The system is designed to run on a standard Windows PC with **16 GB RAM**, without relying on external LLM APIs.

## Key Features

- **Local LLM inference** — Run quantized language models through Ollama without sending data to external AI services.
- **Natural Language to SQL** — Translate analytical questions into executable SQL queries.
- **Database Integration** — Connect to PostgreSQL, with an extensible architecture for additional databases such as Vertica.
- **Agentic Workflows** — Use LangGraph to coordinate multi-step analytical tasks, tool execution, and error handling.
- **Skills-Based Architecture** — Define reusable analytical instructions, business rules, and domain-specific workflows.
- **Data Analysis** — Process query results using Python and pandas.
- **SQL Safety** — Restrict database operations to authorized, read-only queries.
- **Reproducible Environment** — Automate installation, configuration, database initialization, and testing.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Local LLM | Qwen3 4B (4-bit quantized) |
| Model Runtime | Ollama |
| Agent Framework | LangGraph |
| Database | PostgreSQL |
| Data Processing | pandas |
| Database Connectivity | SQLAlchemy |
| Containerization | Docker Compose |
| Testing | pytest |
| Operating System | Windows |

## System Architecture

```text
                  User
                   |
                   v
          Natural Language Query
                   |
                   v
             LangGraph Agent
                   |
             Local LLM (Ollama)
                   |
         +---------+----------+
         |         |          |
         v         v          v
       Skills   Database    Python
                 Tools       Tools
         |         |          |
         +---------+----------+
                   |
                   v
           SQL Validation
                   |
                   v
             PostgreSQL
                   |
                   v
           Query Results
                   |
                   v
         Analysis & Reporting
```

## Project Structure

```text
local-ai-data-analyst/
├── agent/                  # Agent logic and tool orchestration
├── skills/                 # Domain-specific analytical skills
├── database/               # Database schema and synthetic data
├── metadata/               # Database metadata and metric definitions
├── tests/                  # Unit and integration tests
├── scripts/                # Setup and startup scripts
├── .github/workflows/      # CI workflows
├── docker-compose.yml      # PostgreSQL container configuration
├── pyproject.toml          # Python dependencies
├── .env.example            # Environment configuration template
└── README.md
```

## Synthetic Test Database

The project includes a simulated consumer lending database for developing and evaluating the agent.

Planned tables:

| Table | Description |


The dataset will contain synthetic records, allowing safe experimentation with realistic credit risk scenarios.

## Example Analytical Tasks

The agent is intended to support questions such as:

- "Calculate the average amount by month."
- "Show the distribution of approved applications by PD bucket."
- "Compare delinquency rates across customer segments."
- "Check the dataset for missing values and duplicates."

The agent should generate SQL, execute authorized queries, validate results, and explain its findings.

## Getting Started

### Prerequisites

- Windows 10/11
- At least 16 GB RAM recommended
-
