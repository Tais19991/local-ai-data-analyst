from langchain_core.tools import tool
from sqlalchemy.exc import SQLAlchemyError

from agent.db import (
    list_tables,
    describe_table,
    execute_sql,
)


@tool
def get_database_tables() -> list[str]:
    """
    List available tables in the Titanic database.

    Use this tool first when you need to discover
    which tables are available for SQL queries.
    """
    return list_tables()


@tool
def get_table_schema(table_name: str) -> list[dict]:
    """
    Get column names, data types, and nullability
    for a table in the Titanic schema.

    Args:
        table_name: Table name without schema prefix,
                    for example 'passengers'.
    """
    return describe_table(table_name)


@tool
def run_sql_query(query: str) -> dict:
    """
    Execute a read-only PostgreSQL SELECT query.

    If execution fails, inspect the returned error
    and correct the SQL before trying again.

    Args:
        query: PostgreSQL SELECT query.
    """
    try:
        rows = execute_sql(query)

        return {
            "success": True,
            "rows": rows,
        }

    except (SQLAlchemyError, ValueError) as error:
        return {
            "success": False,
            "error": str(error),
            "query": query,
        }


DATABASE_TOOLS = [
    get_database_tables,
    get_table_schema,
    run_sql_query,
]
