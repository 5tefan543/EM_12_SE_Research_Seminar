from google import genai
from google.genai import types
from .base import AIService

class GoogleAIService(AIService):
    def __init__(self, api_key: str, model: str):
        self.provider = "google"
        self.model = model

        if not api_key:
            raise ValueError("API key is required for Google AI Service")
        
        self._client = genai.Client(api_key=api_key)

    async def _generate_response(self, instructions: str, prompt: str) -> str:
        response = await self._client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=instructions,
            ),
        )

        return response.text