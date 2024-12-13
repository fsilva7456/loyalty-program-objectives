from pydantic import BaseModel, Field
from typing import List, Optional

class CompetitorInfo(BaseModel):
    name: str = Field(..., description="Competitor company name")
    loyalty_program_description: Optional[str] = Field(None, description="Description of competitor's loyalty program")
    strengths: Optional[List[str]] = Field(None, description="Key strengths of competitor's program")
    weaknesses: Optional[List[str]] = Field(None, description="Key weaknesses of competitor's program")

class LoyaltyAnalysisRequest(BaseModel):
    company_name: str = Field(..., description="Your company name")
    industry: str = Field(..., description="Industry sector (e.g., retail, hospitality, finance)")
    business_type: str = Field(..., description="Type of business (e.g., B2C, B2B, hybrid)")
    customer_segments: List[str] = Field(..., description="Target customer segments")
    current_loyalty_program: Optional[str] = Field(None, description="Description of current loyalty program if any")
    current_challenges: Optional[List[str]] = Field(None, description="Current challenges with customer loyalty")
    business_goals: Optional[List[str]] = Field(None, description="Key business goals")
    competitors: List[CompetitorInfo] = Field(..., description="Information about key competitors")
    max_tokens: Optional[int] = Field(2000, description="Maximum tokens in the response")
    temperature: Optional[float] = Field(0.7, description="Temperature for response generation")

    def format_prompt(self) -> str:
        prompt = f"Analyze and suggest the top 5 loyalty program objectives for {self.company_name}, " \
                f"a {self.business_type} business in the {self.industry} industry.\n\n"
        
        prompt += "Customer Segments:\n"
        for segment in self.customer_segments:
            prompt += f"- {segment}\n"
        
        if self.current_loyalty_program:
            prompt += f"\nCurrent Loyalty Program:\n{self.current_loyalty_program}\n"
        
        if self.current_challenges:
            prompt += "\nCurrent Challenges:\n"
            for challenge in self.current_challenges:
                prompt += f"- {challenge}\n"
        
        if self.business_goals:
            prompt += "\nBusiness Goals:\n"
            for goal in self.business_goals:
                prompt += f"- {goal}\n"
        
        prompt += "\nCompetitor Analysis:\n"
        for competitor in self.competitors:
            prompt += f"\n{competitor.name}:"
            if competitor.loyalty_program_description:
                prompt += f"\nProgram: {competitor.loyalty_program_description}"
            if competitor.strengths:
                prompt += "\nStrengths:"
                for strength in competitor.strengths:
                    prompt += f"\n- {strength}"
            if competitor.weaknesses:
                prompt += "\nWeaknesses:"
                for weakness in competitor.weaknesses:
                    prompt += f"\n- {weakness}"
            prompt += "\n"
        
        prompt += "\nPlease provide the top 5 specific, measurable loyalty program objectives that consider our " \
                 "company's context, competitive landscape, and business goals. For each objective, " \
                 "provide a clear rationale that explains how it addresses our specific needs and " \
                 "competitive position."
        
        return prompt
