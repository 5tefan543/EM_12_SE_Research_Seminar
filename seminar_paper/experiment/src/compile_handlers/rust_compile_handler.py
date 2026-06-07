import asyncio
from pathlib import Path

from .base import CompileHandler, CompilationResult


class RustCompileHandler(CompileHandler):
    def __init__(self, edition: str = "2021", timeout_seconds: float = 10.0):
        self.comment_symbol = "// "
        self._edition = edition
        self._timeout_seconds = timeout_seconds

    async def _compile(self, source_code_path: Path) -> CompilationResult:
        if not source_code_path.exists() or not source_code_path.is_file():
            raise FileNotFoundError(f"Rust source file not found: {source_code_path}")

        output_path = source_code_path.with_suffix(".rmeta")

        command = [
            "rustc",
            f"--edition={self._edition}",
            "--crate-type",
            "lib",
            "--emit=metadata",
            str(source_code_path),
            "-o",
            str(output_path),
        ]

        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self._timeout_seconds,
            )

            # Clean up the output file if it was created, since we only care about the compilation result
            output_path.unlink(missing_ok=True)

        except asyncio.TimeoutError:
            return CompilationResult(
                message=f"Rust compilation timed out after {self._timeout_seconds} seconds.",
                is_failed=True,
            )

        except FileNotFoundError:
            return CompilationResult(
                message="Rust compiler not found. Make sure `rustc` is installed and available in PATH.",
                is_failed=True,
            )

        is_failed = process.returncode != 0

        stdout_text = stdout.decode("utf-8", errors="replace").strip()
        stderr_text = stderr.decode("utf-8", errors="replace").strip()

        message_parts = []

        if stderr_text:
            message_parts.append(f"\nCompiler stderr:\n")
            message_parts.append(stderr_text)

        if stdout_text:
            message_parts.append(f"\nCompiler stdout:\n")
            message_parts.append(stdout_text)

        message = "\n".join(message_parts)
        message_commented = self._comment_text(message)

        full_message = (
            f"\n\n{self.comment_symbol}Rust compilation {'failed' if is_failed else 'succeeded'}!\n"
            f"{message_commented}"
        )

        return CompilationResult(
            message=full_message,
            is_failed=is_failed,
        )
    
    def _comment_text(self, text: str) -> str:
        return "\n".join(
            f"{self.comment_symbol}{line}"
            for line in text.splitlines()
        )