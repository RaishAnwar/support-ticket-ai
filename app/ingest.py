import sqlite3
import pandas as pd

from app.config import CSV_PATH, DB_PATH


def load_data():
    df = pd.read_csv(CSV_PATH)

    connection = sqlite3.connect(DB_PATH)

    df.to_sql(
        "support_tickets",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print(f"Loaded {len(df)} tickets into the database.")


if __name__ == "__main__":
    load_data()