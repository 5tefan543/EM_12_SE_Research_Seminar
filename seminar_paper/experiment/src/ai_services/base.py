from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GenerationResult:
    content: str
    is_failed: bool


class AIService(ABC):
    provider: str
    model: str

    async def generate_response(self, instructions: str, prompt: str, prompt_path: Path) -> GenerationResult:
        try:
            content = await self._generate_response(instructions, prompt)
            print(
                f"Generation successful:\n"
                f"Provider: {self.provider} | "
                f"Model: {self.model} | "
                f"Prompt: {prompt_path}\n\n"
            )
            return GenerationResult(content=content, is_failed=False)

        except Exception as error:
            error_message = (
                f"Generation FAILED:\n"
                f"Provider: {self.provider} | "
                f"Model: {self.model} | "
                f"Prompt: {prompt_path}\n\n"
                f"---- ERROR DETAILS ---\n"
                f"Error type: {type(error).__name__}\n"
                f"Error message: {error}\n\n"
            )

            print(error_message)
            return GenerationResult(content=error_message, is_failed=True)

    @abstractmethod
    async def _generate_response(self, instructions: str, prompt: str) -> str:
        ...
