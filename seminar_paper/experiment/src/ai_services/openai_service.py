from openai import AsyncOpenAI
from .base import AIService

class OpenAIService(AIService):
    def __init__(self, api_key: str, model: str):
        self.provider = "openai"
        self.model = model

        if not api_key:
            raise ValueError("API key is required for OpenAI Service")
        
        self._client = AsyncOpenAI(api_key=api_key)

    async def _generate_response(self, instructions: str, prompt: str) -> str:
        response = await self._client.responses.create(
            model=self.model,
            instructions=instructions,
            input=prompt,
        )
        return response.output_text
