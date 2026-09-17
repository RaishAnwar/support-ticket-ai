import sqlite3
import pandas as pd

from app.config import DB_PATH, IQR_MULTIPLIER, CRITICAL_TICKET_LIMIT_HOURS


def detect_anomalies():
    connection = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(
            """
            SELECT ticket_id, resolution_time_hrs
            FROM support_tickets
            WHERE resolution_time_hrs IS NOT NULL
            """,
            connection
        )

        q1 = df["resolution_time_hrs"].quantile(0.25)
        q3 = df["resolution_time_hrs"].quantile(0.75)

        iqr = q3 - q1
        upper_limit = q3 + (IQR_MULTIPLIER * iqr)

        anomalies = df[
            df["resolution_time_hrs"] > upper_limit
        ]

        # filter anmalies that are critical and have been open for more than 24 hours
        critical_query = f"""
        SELECT ticket_id, created_at, priority, status
        FROM support_tickets
        WHERE priority = 'Critical'
          AND status != 'Resolved'
          AND datetime(created_at) <= datetime('now', '-{CRITICAL_TICKET_LIMIT_HOURS} hours');
        """
        

        critical_tickets = connection.execute(critical_query).fetchall()

        print("Critical tickets that have been open for more than 24 hours:")
        for ticket in critical_tickets:
            print(ticket)

        return {
            "long_resolution_anomalies": anomalies.to_dict(orient="records"),
            "critical_unresolved_over_24h": critical_tickets,
         }

    finally:
        connection.close()

if __name__ == "__main__":
    result = detect_anomalies()

    print(f"Long resolution anomalies: {len(result['long_resolution_anomalies'])}")

    print("Critical unresolved tickets older than 24 hours:")
    for ticket in result["critical_unresolved_over_24h"]:
        print(ticket)