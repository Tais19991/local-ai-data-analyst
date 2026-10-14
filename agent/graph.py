"""LangGraph tool-calling agent."""
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from .config import Settings
from .db import Database
from .prompts import SYSTEM_PROMPT


def build_agent(settings: Settings | None = None):
    settings = settings or Settings()
    database = Database(settings)

    @tool
    def list_tables() -> list[str]:
        """List permitted tables and views in the PostgreSQL public schema."""
        return database.list_tables()

    @tool
    def describe_table(table: str) -> list[dict]:
        """Get column names and types for an existing public table or view."""
        return database.describe_table(table)

    @tool
    def execute_sql(sql: str) -> dict:
        """Execute a single read-only SELECT query with a row and time limit."""
        return database.execute_query(sql)

    model = ChatOllama(model=settings.model, base_url=settings.base_url, temperature=0)
    return create_react_agent(model, [list_tables, describe_table, execute_sql], prompt=SYSTEM_PROMPT)
