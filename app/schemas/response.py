from pydantic import BaseModel
from typing import List, Dict, Any

class ObjectiveWithRationale(BaseModel):
    objective: str
    rationale: str

class LoyaltyAnalysisResponse(BaseModel):
    company_name: str
    industry: str
    business_type: str
    objectives: List[ObjectiveWithRationale]
    metadata: Dict[str, Any]
