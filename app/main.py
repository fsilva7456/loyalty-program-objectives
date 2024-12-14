from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services.openai_service import OpenAIService
from app.config import Settings, get_settings
from app.schemas.request import LoyaltyAnalysisRequest
from app.schemas.response import LoyaltyAnalysisResponse, ObjectiveWithRationale
import json
import re

app = FastAPI(
    title="Loyalty Program Objectives API",
    description="AI-powered API for analyzing and suggesting loyalty program objectives",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

def parse_objectives(text: str) -> list:
    """Parse objectives from text when JSON parsing fails."""
    objectives = []
    current_obj = {}
    
    # Split text into sections that look like objectives
    sections = re.split(r'\d+\. ', text)
    sections = [s.strip() for s in sections if s.strip()]
    
    for section in sections[:5]:  # Take only top 5
        parts = section.split('Rationale:', 1)
        if len(parts) == 2:
            objective = parts[0].strip()
            rationale = parts[1].strip()
        else:
            objective = parts[0].strip()
            rationale = "Not provided"
            
        objectives.append({
            "objective": objective,
            "rationale": rationale
        })
    
    return objectives

@app.post("/api/v1/analyze-objectives",
    response_model=LoyaltyAnalysisResponse,
    description="Analyze and suggest loyalty program objectives based on company and competitor analysis")
async def analyze_objectives(
    request: LoyaltyAnalysisRequest,
    settings: Settings = Depends(get_settings)
):
    try:
        openai_service = OpenAIService(settings.openai_api_key)
        
        # Generate system prompt for loyalty program analysis
        system_prompt = (
            "You are an expert in loyalty program strategy, customer retention, and competitive analysis. "
            "Analyze the provided information and suggest the top 5 most impactful loyalty program objectives. "
            "Format each objective as:\n"
            "1. [Objective text]\nRationale: [Rationale text]\n\n"
            "2. [Objective text]\nRationale: [Rationale text]\n\n"
            "And so on for 5 objectives. Consider:\n"
            "- Customer engagement and retention\n"
            "- Competitive differentiation\n"
            "- Revenue generation\n"
            "- Brand loyalty\n"
            "- Customer data utilization"
        )
        
        # Process the query
        response = await openai_service.get_analysis(
            user_prompt=request.format_prompt(),
            system_prompt=system_prompt,
            max_tokens=request.max_tokens or 2000,
            temperature=request.temperature or 0.7
        )
        
        # Parse the response
        try:
            # First try to parse as JSON
            objectives = []
            parsed_objectives = parse_objectives(response)
            objectives = [
                ObjectiveWithRationale(**obj)
                for obj in parsed_objectives
            ]
            
            # Return structured response
            return LoyaltyAnalysisResponse(
                company_name=request.company_name,
                industry=request.industry,
                business_type=request.business_type,
                objectives=objectives,
                metadata={
                    "model": "gpt-4-turbo-preview",
                    "max_tokens": request.max_tokens or 2000,
                    "temperature": request.temperature or 0.7
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse AI response: {str(e)}. Response: {response}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
