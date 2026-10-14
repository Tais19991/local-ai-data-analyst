"""Strict SQL gate for the initial PostgreSQL-only MVP."""
import sqlglot
from sqlglot import exp


def validate_sql(sql: str) -> str:
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("SQL must be non-empty")
    statements = sqlglot.parse(sql, read="postgres")
    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Exactly one SQL statement is allowed")
    root = statements[0]
    if not isinstance(root, (exp.Select, exp.Union)):
        raise ValueError("Only SELECT queries are permitted")
    forbidden = (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create, exp.Alter,
                 exp.Command, exp.Copy, exp.Merge, exp.Truncate, exp.Into)
    if any(root.find(t) is not None for t in forbidden):
        raise ValueError("SQL contains a prohibited operation")
    # Disallow calls to arbitrary DB functions (including side-effect functions).
    # An allowlist can be expanded after testing.
    allowed_functions = {"COUNT", "SUM", "AVG", "MIN", "MAX", "ROUND", "COALESCE", "DATE_TRUNC", "ABS"}
    for fn in root.find_all(exp.Func):
        if fn.sql_name().upper() not in allowed_functions:
            raise ValueError(f"Function not allowed: {fn.sql_name()}")
    for table in root.find_all(exp.Table):
        if table.db and table.db.lower() != "public":
            raise ValueError("Only public schema is permitted")
    return root.sql(dialect="postgres")
