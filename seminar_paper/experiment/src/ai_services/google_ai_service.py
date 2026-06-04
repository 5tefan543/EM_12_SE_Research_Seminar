from google import genai
from .base import AIService
from typing import Tuple


class GoogleAIService(AIService):
    def __init__(self, api_key: str, model: str, temperature: float):
        self.provider = "google"
        self.model = model
        self.temperature = temperature

        if not api_key:
            raise ValueError("API key is required for Google AI Service")

        self._client = genai.Client(api_key=api_key)

    async def _generate_response(self, instructions: str, prompt: str, state_id: str = None) -> Tuple[str, str]:

        if state_id is None:
            interaction = self._client.interactions.create(
                input=prompt,
                model=self.model,
                system_instruction=instructions,
                generation_config={
                    "temperature": self.temperature
                }
            )

            return interaction.id, interaction.output_text

        interaction = self._client.interactions.create(
            input=prompt,
            model=self.model,
            previous_interaction_id=state_id,
            system_instruction=instructions,
            generation_config={
                "temperature": self.temperature
            }
        )

        return interaction.id, interaction.output_text

    async def _delete_state(self, state_id: str) -> None:
        self._client.interactions.delete(state_id)
