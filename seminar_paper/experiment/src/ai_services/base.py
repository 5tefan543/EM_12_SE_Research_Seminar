from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from logging import getLogger
logger = getLogger(__name__)

@dataclass
class GenerationResult:
    state_id: str
    content: str | None = None
    error: Exception | None = None
    is_failed: bool = False


class AIService(ABC):
    provider: str
    model: str
    temperature: float

    async def generate_response(self, instructions: str, prompt: str, state_id: str = None) -> GenerationResult:
        try:
            state_id, content = await self._generate_response(instructions, prompt, state_id)
            return GenerationResult(state_id=state_id, content=content)

        except Exception as error:
            return GenerationResult(state_id=state_id, error=error, is_failed=True)

    @abstractmethod
    async def _generate_response(self, instructions: str, prompt: str, state_id: str = None) -> Tuple[str, str]:
        ...

    async def delete_state(self, state_id: str) -> None:
        try:
            await self._delete_state(state_id)
        except Exception as error:
            logger.error(f"Error deleting state {state_id} for provider {self.provider}: {error}")

    @abstractmethod
    async def _delete_state(self, state_id: str) -> None:
        ...
