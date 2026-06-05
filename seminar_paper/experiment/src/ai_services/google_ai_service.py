from google import genai
from .base import AIService
from typing import Optional, Tuple
import asyncio


class GoogleAIService(AIService):
    def __init__(self, api_key: str, model: str, temperature: float):
        self.provider = "google"
        self.model = model
        self.temperature = temperature

        if not api_key:
            raise ValueError("API key is required for Google AI Service")

        self._client = genai.Client(api_key=api_key)

    async def _generate_response(
        self,
        instructions: str,
        prompt: str,
        state_id: Optional[str] = None,
    ) -> Tuple[str, str]:

        kwargs = {
            "input": prompt,
            "model": self.model,
            "system_instruction": instructions,
            "generation_config": {
                "temperature": self.temperature,
            },
        }

        if state_id is not None:
            kwargs["previous_interaction_id"] = state_id

        interaction = await asyncio.to_thread(
            self._client.interactions.create,
            **kwargs,
        )

        return interaction.id, interaction.output_text

    async def _delete_state(self, state_id: str) -> None:
        await asyncio.to_thread(
            self._client.interactions.delete,
            state_id,
        )
