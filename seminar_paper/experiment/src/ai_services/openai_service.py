from typing import Optional, Tuple
from openai import AsyncOpenAI
from .base import AIService


class OpenAIService(AIService):
    def __init__(self, api_key: str, model: str, temperature: float):
        self.provider = "openai"
        self.model = model
        self.temperature = temperature

        if not api_key:
            raise ValueError("API key is required for OpenAI Service")

        self._client = AsyncOpenAI(api_key=api_key)

    async def _generate_response(
        self,
        instructions: str,
        prompt: str,
        state_id: Optional[str] = None,
    ) -> Tuple[str, str]:

        if state_id is None:
            conversation = await self._client.conversations.create()
            state_id = conversation.id

        kwargs = {
            "model": self.model,
            "conversation": state_id,
            "instructions": instructions,
            "input": prompt,
            "temperature": self.temperature,
        }

        response = await self._client.responses.create(**kwargs)

        return state_id, response.output_text

    async def _delete_state(self, state_id: str) -> None:
        await self._client.conversations.delete(state_id)
