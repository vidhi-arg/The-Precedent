from pydantic import BaseModel
from typing import List, Dict

class ConflictRequest(BaseModel):
    country: str
    issue_description: str

class Case(BaseModel):
    name: str
    year: int

class LegalResponse(BaseModel):
    article: str
    cases: List[Case]
    escalation_paths: List[str]
    people_involved: Dict[str, str]
    suggested_actions: List[str]
