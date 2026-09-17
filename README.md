# Support Ticket AI

AI-powered customer support ticket analysis system that allows users to query support ticket data using natural language and detect potential anomalies.

## Features

- Load customer support ticket data from CSV into SQLite
- Ask natural-language questions about the ticket data
- Use an LLM to convert natural-language questions into SQL
- Execute safe read-only SQL queries
- Detect unusually long resolution times using IQR-based anomaly detection
- Flag unresolved Critical tickets older than 24 hours
- REST API using FastAPI
- Minimal web UI using Streamlit
- API health check endpoint

## Architecture

```text
support_tickets.csv
        |
        v
   Pandas Ingestion
        |
        v
   SQLite Database
    (tickets.db)
        |
        +----------------------+
        |                      |
        v                      v
 Natural Language Query   Anomaly Detection
        |                      |
        v                      |
     Groq LLM                  |
        |                      |
        v                      v
   Generated SQL        Python + SQLite
        |                      |
        +----------+-----------+
                   |
                   v
              FastAPI API
                   |
                   v
             Streamlit UI
```

## Design Decisions

### SQLite for Data Storage

SQLite is used because the provided dataset is relatively small and does not require a separate database server.

### LLM for Natural-Language Queries

The LLM is used to understand natural-language questions and convert them into SQL queries that can be executed against the SQLite database.

### Deterministic Anomaly Detection

The LLM is not used for anomaly detection or numeric calculations. Anomaly detection uses deterministic Python and SQL logic so that the results are reproducible and explainable.

### Separation of Responsibilities

FastAPI provides the REST API layer, while Streamlit provides the user interface. The core query and anomaly-detection logic is kept separately inside the application modules.

## Technology Stack

- Python
- Pandas
- SQLite
- FastAPI
- Streamlit
- Groq LLM
- SQL
- Pydantic
- python-dotenv
- Requests

## How the System Works

1. The CSV file is loaded using Pandas.
2. The ticket data is stored in a SQLite database.
3. A user enters a question in natural language.
4. The question is sent to the Groq LLM.
5. The LLM generates a SQL `SELECT` query based on the database schema.
6. The application validates and executes the generated SQL query.
7. The query result is returned through the FastAPI API.
8. The Streamlit UI displays the result in a readable format.
9. The anomaly detection module separately analyzes the ticket data using deterministic rules.

## Dataset

The system uses the provided `support_tickets.csv` dataset containing 500 customer support tickets.

### Database Table

The CSV data is stored in a SQLite table named `support_tickets`.

### Schema

| Column | Description |
|---|---|
| `ticket_id` | Unique ticket identifier |
| `created_at` | Ticket creation timestamp |
| `category` | Billing, Technical, or General |
| `priority` | Low, Medium, High, or Critical |
| `status` | Open, Resolved, or Escalated |
| `response_time_hrs` | Response time in hours |
| `resolution_time_hrs` | Resolution time in hours; null for unresolved tickets |
| `agent_id` | Support agent identifier |
| `customer_rating` | Customer rating; null for unresolved tickets |
| `issue_summary` | Short description of the customer issue |

## Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd support-ticket-ai
```

## 2. Create a Virtual Environment

python -m venv .venv

## Activate it on Windows:

.venv\Scripts\activate

## 3. Install Dependencies

pip install -r requirements.txt

## 4. Configure the LLM

**Create a .env file in the project root:**

LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key

## 5. Load the Dataset

# Run:

python -m app.ingest

### 6. Start the Application

Run a single command from the project root:

```bash
python run.py
```

## REST API

**The application provides three REST API endpoints.**

### Health Check

```http
GET /health 
```

## Natural-Language Query
POST /query

## Anomaly Detection
GET /anomalies

### 1. Example Queries

The system supports natural-language questions such as:

### 1. Open Tickets

**Question:**

How many tickets are currently open?

**Output:**

```text
111
```
### 2. Agent Performance

**Question:**

Which agent resolved the most tickets this month?

The system generates a SQL query to calculate the number of resolved tickets for each agent and returns the agent with the highest count.

### 3. Critical Tickets

**Question:**

Show me all Critical tickets not resolved within 12 hours.

The system filters Critical tickets and checks their resolution time.

### 4. Customer Rating

**Question:**

What is the average customer rating for Technical category tickets?

The system calculates the average customer rating for tickets in the Technical category.


## Anomaly Detection

The system detects two types of potential anomalies:

### 1. Long Resolution Time

The system uses the Interquartile Range (IQR) method to identify tickets with unusually high resolution times.

The upper threshold is calculated as:

```text
Upper Limit = Q3 + (1.5 × IQR)
```
 ## Critical Unresolved Tickets

**The system checks for Critical-priority tickets that are not resolved and have remained unresolved for more than 24 hours**.

**These tickets are flagged because they may require attention from the support team.**

## User Interface

The system includes a minimal Streamlit web interface.

The UI provides:

- A natural-language question input
- Query results displayed in a table
- Generated SQL displayed for transparency
- Anomaly detection results
- Counts of detected anomalies
- API health status

The UI communicates with the FastAPI backend through REST API endpoints.

## SQL Safety

The natural-language query system is designed for read-only database access.

Before execution, the generated SQL is checked to ensure that it starts with a `SELECT` statement.

The system only provides access to the `support_tickets` table and does not allow data-modifying operations such as:

- INSERT
- UPDATE
- DELETE
- DROP
- ALTER

Detailed query results are limited to a maximum number of rows.

## Error Handling

The application handles common errors during query execution and API communication.

If an invalid or unsupported SQL query is generated, the backend returns an error instead of executing it.

The Streamlit UI also displays a clear error message when the FastAPI backend is not reachable.

## Project Structure

```text
support-ticket-ai/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── ingest.py
│   ├── llm.py
│   ├── nl_query.py
│   └── anomaly.py
├── data/
│   ├── support_tickets.csv
│   └── tickets.db
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── main.py
└── ui.py
└── run.py
```

## Known Limitations

- The system currently works with the provided support ticket dataset.
- Natural-language SQL generation depends on the LLM producing valid SQL.
- The anomaly detection rules are based on fixed statistical and business thresholds.
- The current UI is intentionally minimal and focused on the core requirements.

## What I’d Do With More Time

- Add more advanced natural-language query validation.
- Add authentication and API access controls.
- Add more anomaly detection rules and configurable thresholds.
- Add automated tests for the API and core application modules.
- Improve the Streamlit dashboard with additional visualizations.
- Add support for larger datasets and production-scale databases.