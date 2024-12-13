from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services.openai_service import OpenAIService
from app.config import Settings, get_settings
from app.schemas.request import LoyaltyAnalysisRequest
from app.schemas.response import LoyaltyAnalysisResponse

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
    description="Analyze and suggest loyalty program objectives based on input parameters")
async def analyze_objectives(
    request: LoyaltyAnalysisRequest,
    settings: Settings = Depends(get_settings)
):
    try:
        openai_service = OpenAIService(settings.openai_api_key)
        
        # Generate system prompt for loyalty program analysis
        system_prompt = (
            "You are an expert in loyalty program strategy and customer retention. "
            "Analyze the provided information and suggest specific, actionable objectives "
            "that align with the business goals and customer segments. Consider factors like:"
            "\n- Customer engagement and retention"
            "\n- Revenue generation and profitability"
            "\n- Brand loyalty and advocacy"
            "\n- Competitive differentiation"
        )
        
        # Process the query
        response = await openai_service.get_analysis(
            user_prompt=request.format_prompt(),
            system_prompt=system_prompt,
            max_tokens=request.max_tokens or 1000,
            temperature=request.temperature or 0.7
        )
        
        # Return structured response
        return LoyaltyAnalysisResponse(
            industry=request.industry,
            business_type=request.business_type,
            customer_segments=request.customer_segments,
            objectives=response,
            metadata={
                "model": "gpt-4-turbo-preview",
                "max_tokens": request.max_tokens or 1000,
                "temperature": request.temperature or 0.7
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
