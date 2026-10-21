
from agent.tools import (
    get_database_tables,
    get_table_schema,
    run_sql_query,
)

print("1. Available tables:")
print(get_database_tables.invoke({}))

print("\n2. Table schema:")
print(
    get_table_schema.invoke({
        "table_name": "passengers"
    })
)

print("\n3. SQL query:")
print(
    run_sql_query.invoke({
        "query": """
            SELECT
                pclass,
                COUNT(*) AS passengers,
                ROUND(
                    AVG(survived::numeric) * 100,
                    2
                ) AS survival_rate_pct
            FROM titanic.passengers
            GROUP BY pclass
            ORDER BY pclass
        """
    })
)
