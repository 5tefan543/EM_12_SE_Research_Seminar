from .base import CompileHandler
from .rust_compile_handler import RustCompileHandler
from enum import Enum

class CompileHandlerType(Enum):
    RUST = "rust"

class CompileHandlerFactory:
    @staticmethod
    def create_handler(handler_type: CompileHandlerType) -> CompileHandler:

        match handler_type:
            case CompileHandlerType.RUST:
                return RustCompileHandler()
            case _:
                raise ValueError(f"Unsupported Compile Handler Type: {handler_type}")
