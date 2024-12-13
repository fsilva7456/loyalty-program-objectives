from pydantic import BaseModel
from typing import List, Dict, Any

class LoyaltyAnalysisResponse(BaseModel):
    industry: str
    business_type: str
    customer_segments: List[str]
    objectives: str
    metadata: Dict[str, Any]
