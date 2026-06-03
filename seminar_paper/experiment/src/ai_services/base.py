from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class GenerationResult:
    content: str | None = None
    error: Exception | None = None
    is_failed: bool = False


class AIService(ABC):
    provider: str
    model: str

    async def generate_response(self, instructions: str, prompt: str) -> GenerationResult:
        try:
            content = await self._generate_response(instructions, prompt)
            return GenerationResult(content=content)

        except Exception as error:
            return GenerationResult(error=error, is_failed=True)

    @abstractmethod
    async def _generate_response(self, instructions: str, prompt: str) -> str:
        ...
