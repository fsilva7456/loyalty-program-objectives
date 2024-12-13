# Loyalty Program Objectives API

An AI-powered API for analyzing and suggesting loyalty program objectives using FastAPI and OpenAI.

## Features

- FastAPI with async/await support
- OpenAI GPT-4 Turbo integration
- Industry-specific loyalty program analysis
- Customizable objectives based on business context
- Detailed response with actionable insights

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

2. Make a test request:
```bash
curl -X POST "http://localhost:8000/api/v1/analyze-objectives" \
     -H "Content-Type: application/json" \
     -d '{
           "industry": "retail",
           "business_type": "B2C",
           "customer_segments": ["millennials", "frequent shoppers"],
           "current_challenges": ["low repeat purchase rate"],
           "business_goals": ["increase customer lifetime value"],
           "max_tokens": 1000,
           "temperature": 0.7
         }'
```

## Project Structure

```
loyalty-program-objectives/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── services/
│   │   ├── __init__.py
│   │   └── openai_service.py  # OpenAI integration
│   └── schemas/
│       ├── __init__.py
│       ├── request.py         # Request models
│       └── response.py        # Response models
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

### POST /api/v1/analyze-objectives

Analyzes business context and suggests loyalty program objectives.

#### Request Body
```json
{
  "industry": "string",
  "business_type": "string",
  "customer_segments": ["string"],
  "current_challenges": ["string"],
  "business_goals": ["string"],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### Response
```json
{
  "industry": "string",
  "business_type": "string",
  "customer_segments": ["string"],
  "objectives": "string",
  "metadata": {
    "model": "string",
    "max_tokens": 0,
    "temperature": 0
  }
}
```

## License

MIT