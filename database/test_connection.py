from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

# 1. Load database configuration from .env
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is missing from .env")

# 2. Create the database connection engine
engine = create_engine(
    database_url,
    connect_args={"connect_timeout": 5},
)

# 3. Execute a simple SQL query
with engine.connect() as connection:
    result = connection.execute(
        text("SELECT COUNT(*) FROM titanic.passengers")
    )
    print("Passengers:", result.scalar_one())

# 4. Retrieve database metadata
inspector = inspect(engine)

print("\nAvailable tables:")

for table_name in inspector.get_table_names(schema="titanic"):
    print(f"\nTable: titanic.{table_name}")

    for column in inspector.get_columns(
        table_name,
        schema="titanic",
    ):
        print(f"  {column['name']}: {column['type']}")

engine.dispose()
