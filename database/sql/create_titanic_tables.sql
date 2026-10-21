
CREATE SCHEMA IF NOT EXISTS titanic;

CREATE TABLE IF NOT EXISTS titanic.passengers (
    passenger_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    survived INTEGER,
    pclass INTEGER,
    sex VARCHAR(20),
    age NUMERIC,
    sibsp INTEGER,
    parch INTEGER,
    fare NUMERIC,
    embarked VARCHAR(10)
);
