from pydantic import BaseModel, Field
from typing import List, Optional

class LoyaltyAnalysisRequest(BaseModel):
    industry: str = Field(..., description="Industry sector (e.g., retail, hospitality, finance)")
    business_type: str = Field(..., description="Type of business (e.g., B2C, B2B, hybrid)")
    customer_segments: List[str] = Field(..., description="Target customer segments")
    current_challenges: Optional[List[str]] = Field(None, description="Current challenges with customer loyalty")
    business_goals: Optional[List[str]] = Field(None, description="Key business goals")
    max_tokens: Optional[int] = Field(1000, description="Maximum tokens in the response")
    temperature: Optional[float] = Field(0.7, description="Temperature for response generation")

    def format_prompt(self) -> str:
        prompt = f"Analyze and suggest loyalty program objectives for a {self.business_type} business in the {self.industry} industry.\n\n"
        
        prompt += "Customer Segments:\n"
        for segment in self.customer_segments:
            prompt += f"- {segment}\n"
        
        if self.current_challenges:
            prompt += "\nCurrent Challenges:\n"
            for challenge in self.current_challenges:
                prompt += f"- {challenge}\n"
        
        if self.business_goals:
            prompt += "\nBusiness Goals:\n"
            for goal in self.business_goals:
                prompt += f"- {goal}\n"
        
        prompt += "\nPlease provide specific, measurable objectives for the loyalty program that address these factors."
        
        return prompt
