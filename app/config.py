import os
from dotenv import load_dotenv

load_dotenv()

# LLM settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "openai/gpt-oss-120b"

# Dataset and database
CSV_PATH = "data/support_tickets.csv"
DB_PATH = "data/tickets.db"

# Anomaly detection
CRITICAL_TICKET_LIMIT_HOURS = 24
IQR_MULTIPLIER = 1.5

# Query safety
MAX_QUERY_ROWS = 100