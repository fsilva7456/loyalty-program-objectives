# Loyalty Program Objectives API

An AI-powered API for analyzing and suggesting loyalty program objectives using FastAPI and OpenAI. The API considers your company's context, customer segments, current challenges, and competitor analysis to provide strategic, actionable objectives.

## Features

- FastAPI with async/await support
- OpenAI GPT-4 Turbo integration
- Competitive analysis integration
- Industry-specific loyalty program analysis
- Detailed rationale for each objective
- Structured response format

## Setup

1. Clone the repository:
```bash
git clone https://github.com/fsilva7456/loyalty-program-objectives.git
cd loyalty-program-objectives
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

## Usage

1. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

2. Example request:
```bash
curl -X POST "http://localhost:8000/api/v1/analyze-objectives" \
     -H "Content-Type: application/json" \
     -d '{
           "company_name": "WellnessMart",
           "industry": "retail",
           "business_type": "B2C",
           "customer_segments": [
             "health-conscious millennials",
             "fitness enthusiasts",
             "organic food shoppers"
           ],
           "current_loyalty_program": "Basic points system: 1 point per dollar spent, 100 points = $1 discount",
           "current_challenges": [
             "Low engagement with current program",
             "High competition from specialized health stores",
             "Limited customer data utilization"
           ],
           "business_goals": [
             "Increase customer lifetime value by 30%",
             "Improve retention rate for first-time customers",
             "Drive more frequent store visits"
           ],
           "competitors": [
             {
               "name": "HealthyChoice Market",
               "loyalty_program_description": "Tiered program with health coaching rewards",
               "strengths": [
                 "Personal health coaching sessions",
                 "Integration with fitness apps"
               ],
               "weaknesses": [
                 "High threshold for meaningful rewards",
                 "Limited personalization"
               ]
             },
             {
               "name": "VitaPlus",
               "loyalty_program_description": "Points plus subscription model",
               "strengths": [
                 "Predictable recurring revenue",
                 "Strong mobile app experience"
               ],
               "weaknesses": [
                 "Complex program rules",
                 "Limited flexibility for customers"
               ]
             }
           ]
         }'
```

3. Example response:
```json
{
  "company_name": "WellnessMart",
  "industry": "retail",
  "business_type": "B2C",
  "objectives": [
    {
      "objective": "Implement a three-tiered wellness rewards program with experiential benefits, targeting 50% membership enrollment in 6 months",
      "rationale": "Addresses the need for differentiation from competitors while leveraging our strength in holistic wellness. The tiered structure encourages progression and longer-term engagement, directly impacting customer lifetime value."
    },
    {
      "objective": "Launch a mobile app with personalized health journey tracking, aiming for 40% adoption rate among loyalty members in first quarter",
      "rationale": "Capitalizes on the competitor weakness in personalization while meeting our tech-savvy millennial segment's expectations. The app will also provide valuable customer data for further program optimization."
    }
  ],
  "metadata": {
    "model": "gpt-4-turbo-preview",
    "max_tokens": 2000,
    "temperature": 0.7
  }
}
```

## API Endpoints

### POST /api/v1/analyze-objectives

Analyzes business context and competitor landscape to suggest loyalty program objectives.

#### Request Body Schema
```typescript
{
  company_name: string
  industry: string
  business_type: string
  customer_segments: string[]
  current_loyalty_program?: string
  current_challenges?: string[]
  business_goals?: string[]
  competitors: {
    name: string
    loyalty_program_description?: string
    strengths?: string[]
    weaknesses?: string[]
  }[]
  max_tokens?: number
  temperature?: number
}
```

#### Response Schema
```typescript
{
  company_name: string
  industry: string
  business_type: string
  objectives: {
    objective: string
    rationale: string
  }[]
  metadata: {
    model: string
    max_tokens: number
    temperature: number
  }
}
```

## License

MIT