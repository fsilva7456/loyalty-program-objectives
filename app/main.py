from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services.openai_service import OpenAIService
from app.config import Settings, get_settings
from app.schemas.request import LoyaltyAnalysisRequest
from app.schemas.response import LoyaltyAnalysisResponse, ObjectiveWithRationale
import json

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
            "Your task is to analyze the provided information about a company and its competitors to suggest "
            "the top 5 most impactful loyalty program objectives. For each objective, provide a clear rationale "
            "that explains how it addresses the company's specific needs and competitive position. Consider factors like:"
            "\n- Customer engagement and retention"
            "\n- Competitive differentiation and market positioning"
            "\n- Revenue generation and profitability"
            "\n- Brand loyalty and advocacy"
            "\n- Customer data and insights"
            "\n\nProvide your response in the following JSON format:"
            "\n{\"objectives\": [{\"objective\": \"objective text\", \"rationale\": \"rationale text\"}, ...]}"
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
            parsed_response = json.loads(response)
            objectives = [
                ObjectiveWithRationale(**obj)
                for obj in parsed_response["objectives"]
            ]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse AI response into required format: {str(e)}"
            )
        
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
        raise HTTPException(status_code=500, detail=str(e))
