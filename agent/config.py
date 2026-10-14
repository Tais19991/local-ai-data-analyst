"""Environment-driven application settings."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model: str = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://analyst:analyst@localhost:5432/analytics")
    max_rows: int = int(os.getenv("MAX_QUERY_ROWS", "200"))
    statement_timeout_ms: int = int(os.getenv("STATEMENT_TIMEOUT_MS", "10000"))
