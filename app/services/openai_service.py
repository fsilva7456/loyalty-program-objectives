from openai import AsyncOpenAI
from fastapi import HTTPException

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def get_analysis(
        self,
        user_prompt: str,
        system_prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"OpenAI API error: {str(e)}"
            )
