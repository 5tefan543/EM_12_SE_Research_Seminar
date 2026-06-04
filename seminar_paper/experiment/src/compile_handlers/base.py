from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from logging import getLogger
logger = getLogger(__name__)

@dataclass
class CompilationResult:
    message: str
    is_failed: bool = False


class CompileHandler(ABC):
    comment_symbol: str

    async def compile(self, code: str) -> CompilationResult:
        try:
            return await self._compile(code)

        except Exception as error:
            return CompilationResult(message=str(error), is_failed=True)

    @abstractmethod
    async def _compile(self, code: str) -> CompilationResult:
        ...
