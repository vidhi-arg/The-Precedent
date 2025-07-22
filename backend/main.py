from fastapi import FastAPI, HTTPException
from models import ConflictRequest, LegalResponse
from legal_assistant import query_legal_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Legal AI Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=LegalResponse)
def analyze_conflict(request: ConflictRequest):
    try:
        result = query_legal_llm(request.country, request.issue_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
