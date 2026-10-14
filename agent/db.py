"""Database metadata and read-only execution."""
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from .config import Settings


class Database:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.engine: Engine = create_engine(settings.database_url, pool_pre_ping=True)

    def list_tables(self) -> list[str]:
        inspector = inspect(self.engine)
        return sorted(inspector.get_table_names(schema="public") + inspector.get_view_names(schema="public"))

    def describe_table(self, table: str) -> list[dict]:
        if table not in self.list_tables():
            raise ValueError("Table not found in allowed schema")
        return [{"name": col["name"], "type": str(col["type"]), "nullable": col["nullable"]}
                for col in inspect(self.engine).get_columns(table, schema="public")]

    def execute_query(self, sql: str) -> dict:
        from .tools import validate_sql
        normalized = validate_sql(sql)
        # This is an additional safeguard, not a substitute for read-only DB permissions.
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(text("SET TRANSACTION READ ONLY"))
                conn.execute(text("SET LOCAL statement_timeout = :timeout"), {"timeout": self.settings.statement_timeout_ms})
                result = conn.execute(text(f"SELECT * FROM ({normalized}) AS agent_result LIMIT :max_rows"),
                                      {"max_rows": self.settings.max_rows})
                rows = [dict(row) for row in result.mappings().all()]
                return {"columns": list(result.keys()), "rows": rows, "returned_rows": len(rows),
                        "row_limit": self.settings.max_rows}
