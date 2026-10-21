import pandas as pd
from sqlalchemy import create_engine, text

DATA_URL = (
    "https://raw.githubusercontent.com/"
    "mwaskom/seaborn-data/master/titanic.csv"
)

DATABASE_URL = (
    "postgresql+psycopg://analyst:"
    "analyst_dev_password@localhost:5432/titanic_db"
)

columns = [
    "survived", "pclass", "sex", "age",
    "sibsp", "parch", "fare", "embarked"
]

df = pd.read_csv(DATA_URL, usecols=columns)

engine = create_engine(DATABASE_URL)

with engine.begin() as connection:
    connection.execute(
        text("TRUNCATE TABLE titanic.passengers RESTART IDENTITY")
    )

df.to_sql(
    "passengers",
    engine,
    schema="titanic",
    if_exists="append",
    index=False
)

print(f"Loaded {len(df)} passengers")
