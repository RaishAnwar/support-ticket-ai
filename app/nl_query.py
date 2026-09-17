import sqlite3

from app.config import DB_PATH, MAX_QUERY_ROWS
from app.llm import ask_llm


def get_schema():
    return """
Table: support_tickets

Columns:
- ticket_id
- created_at
- category
- priority
- status
- response_time_hrs
- resolution_time_hrs
- agent_id
- customer_rating
- issue_summary

Possible values:
- category: Billing, Technical, General
- priority: Low, Medium, High, Critical
- status: Open, Resolved, Escalated
"""


def generate_sql(question: str) -> str:
    prompt = f"""
You are a SQL assistant.

Use the following SQLite database schema:

{get_schema()}

Convert the user's question into one SQLite SELECT query.

Rules:
- Return only SQL.
- Use only the support_tickets table.
- Do not INSERT, UPDATE, DELETE, DROP, or ALTER.
- Do not use any other table.
- Limit detailed results to {MAX_QUERY_ROWS} rows.

User question:
{question}
"""

    return ask_llm(prompt).strip()


def execute_query(sql: str):
    sql = sql.strip()

    if not sql.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(sql)

        columns = [
            description[0]
            for description in cursor.description
        ]

        rows = cursor.fetchmany(MAX_QUERY_ROWS)

        return columns, rows

    finally:
        connection.close()


def answer_question(question: str):
    try:
        sql = generate_sql(question)

        columns, rows = execute_query(sql)

        return {
            "question": question,
            "sql": sql,
            "columns": columns,
            "rows": rows,
        }

    except Exception as e:
        return {
            "question": question,
            "error": str(e),
        }