"""Database metadata and read-only execution."""
import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

load_dotenv()


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create and reuse the database engine."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is missing")

    return create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5},
    )


def list_tables(schema: str = "titanic") -> list[str]:
    """List tables in a database schema."""
    inspector = inspect(get_engine())
    return inspector.get_table_names(schema=schema)


def describe_table(
    table_name: str,
    schema: str = "titanic",
) -> list[dict]:
    """Return column names, types and nullability."""
    inspector = inspect(get_engine())

    if table_name not in inspector.get_table_names(schema=schema):
        raise ValueError(f"Unknown table: {schema}.{table_name}")

    columns = inspector.get_columns(table_name, schema=schema)

    return [
        {
            "name": column["name"],
            "type": str(column["type"]),
            "nullable": column["nullable"],
        }
        for column in columns
    ]


def execute_sql(query: str) -> list[dict]:
    """Execute a read-only query and return up to 100 rows."""
    statement = query.strip()

    if not statement.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    with get_engine().connect() as connection:
        result = connection.execute(text(statement))
        return [
            dict(row)
            for row in result.mappings().fetchmany(100)
        ]
