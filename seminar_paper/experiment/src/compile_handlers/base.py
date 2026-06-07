from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from logging import getLogger
logger = getLogger(__name__)

@dataclass
class CompilationResult:
    message: str
    is_failed: bool = False


class CompileHandler(ABC):
    comment_symbol: str

    async def compile(self, source_code_path: Path) -> CompilationResult:
        try:
            return await self._compile(source_code_path)

        except Exception as error:
            return CompilationResult(message=str(error), is_failed=True)

    @abstractmethod
    async def _compile(self, source_code_path: Path) -> CompilationResult:
        ...
