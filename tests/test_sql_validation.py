import pytest
from agent.tools import validate_sql


def test_select_allowed():
    assert "SELECT" in validate_sql("SELECT COUNT(*) FROM public.loans")


@pytest.mark.parametrize("sql", [
    "DELETE FROM loans", "DROP TABLE loans", "SELECT 1; SELECT 2",
    "SELECT pg_sleep(5)", "SELECT * FROM private.clients",
    "WITH x AS (DELETE FROM loans RETURNING *) SELECT * FROM x",
])
def test_unsafe_queries_rejected(sql):
    with pytest.raises(ValueError):
        validate_sql(sql)
