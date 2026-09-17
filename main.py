from fastapi import FastAPI
from app.nl_query import answer_question
from pydantic import BaseModel
from app.anomaly import detect_anomalies



app = FastAPI(
    title="Support Ticket AI",
    description="AI-powered support ticket analysis system",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return{
        "status": "healthy"
    }


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_tickets(request: QueryRequest):
    return answer_question(request.question)


@app.get("/anomalies")
def get_anomalies():
    return detect_anomalies()