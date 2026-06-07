from __future__ import annotations
import asyncio
from dataclasses import dataclass
from pathlib import Path
from config import Config
from ai_services import AIServiceFactory, AIService, GenerationResult
from datetime import datetime, timedelta
import shutil
from compile_handlers import CompileHandlerFactory

from logger import get_logger
logger = get_logger(__name__)


@dataclass(frozen=True)
class Prompt:
    prompt_path: Path
    instruction_path: Path


class Runner:
    logger_indent = "  - "
    request_sleep_time = timedelta(seconds=3)

    def __init__(self, config: Config, clean_output: bool):
        self._config = config
        self._clean_output_dir(clean_output)

    def _clean_output_dir(self, clean_output: bool) -> None:

        if not clean_output:
            return

        output_dir = self._config.dataset.output_dir.resolve()

        if not output_dir.exists():
            logger.info(
                f"Output directory '{output_dir}' does not exist. No cleanup needed.")
            return

        if not output_dir.is_dir():
            raise ValueError(f"Output path is not a directory: {output_dir}")

        shutil.rmtree(output_dir)
        logger.info(f"Cleaned output directory: {output_dir}")

    async def run(self) -> None:
        dataset = self._config.dataset
        self._validate_dataset_dir(dataset.dir_path)
        current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        prompts = self._collect_prompts(
            dataset_dir=dataset.dir_path,
            prompt_file=dataset.prompt_file,
            instruction_file=dataset.instruction_file,
        )

        instruction_cache: dict[Path, str] = {}
        services = AIServiceFactory.create_services(self._config.ai)
        compile_handler = CompileHandlerFactory.create_handler(
            dataset.compile_handler_type)
        
        logger.info(f"Starting experiment with {len(prompts)} prompts.")
        logger.info(f"Dataset directory: {dataset.dir_path}")
        logger.info(f"Output directory: {dataset.output_dir}")
        logger.info(f"Using AI services:")
        for service in services:
            logger.info(
                f"{self.logger_indent}Provider: {service.provider}, Model: {service.model}")
        logger.info(f"Using compile handler: {compile_handler.__class__.__name__}")

        for prompt in prompts:
            prompt_text = prompt.prompt_path.read_text(encoding="utf-8")

            instructions = self._get_instruction_text(
                instruction_path=prompt.instruction_path, instruction_cache=instruction_cache)

            for repetition in range(1, dataset.repetitions + 1):
                for service in services:
                    state_ids = set()
                    current_state_id = None

                    for version in range(1, dataset.max_versions + 1):
                        # Ensure some wait time between requests to avoid hitting rate limits
                        await asyncio.sleep(self.request_sleep_time.total_seconds())

                        service_response = await service.generate_response(instructions, prompt_text, current_state_id)
                        response_file_path = self._build_response_file_path(
                            current_timestamp,
                            dataset.dir_path,
                            dataset.output_dir,
                            prompt.prompt_path,
                            dataset.response_file,
                            service,
                            repetition,
                            version,
                            service_response.is_failed
                        )
                        
                        state_ids.add(service_response.state_id)
                        current_state_id = service_response.state_id

                        messages = self._get_log_messages(
                            service_response, service, prompt.prompt_path, response_file_path)

                        for msg in messages:
                            if service_response.is_failed:
                                logger.error(msg)
                            else:
                                logger.info(msg)

                        response_file_content = self.strip_markdown_code_fence(service_response.content)

                        # Write error message to response file if generation failed and skip compilation
                        if service_response.is_failed:
                            response_file_content = "\n".join(messages)
                            response_file_path.write_text(
                                response_file_content, encoding="utf-8")
                            break

                        # Write the generated response to the response file before compilation
                        response_file_path.write_text(
                            response_file_content, encoding="utf-8")

                        # Compile code
                        compilation_result = await compile_handler.compile(response_file_path)

                        # Append compilation message to the response file
                        with open(response_file_path, "a", encoding="utf-8") as f:
                            f.write(compilation_result.message)

                        # Skip retrying generation if compilation succeeded
                        if not compilation_result.is_failed:
                            logger.info(f"{self.logger_indent}Compilation successful for version {version}")
                            break

                        logger.info(
                            f"{self.logger_indent}Compilation failed for version {version}")
                        logger.debug(
                            f"{self.logger_indent}Compilation error: {compilation_result.message}")

                        # Create a new prompt that includes the compilation error message for the next version
                        prompt_text = (
                            f"Compilation failed with the following error:\n"
                            f"{compilation_result.message}\n\n"
                            f"Please fix the code and try again."
                        )

                        if version == dataset.max_versions:
                            logger.warning(f"{self.logger_indent}Reached maximum versions for this prompt and service. Moving to next prompt.")
                        else:
                            logger.info(f"{self.logger_indent}Retrying generation with updated prompt for version {version + 1}")

                    # Cleanup any remaining states for the current service
                    for state_id in state_ids:
                        await service.delete_state(state_id)

    def _validate_dataset_dir(self, dataset_dir: Path) -> None:
        if not dataset_dir.exists():
            raise FileNotFoundError(
                f"Dataset path '{dataset_dir}' does not exist")

        if not dataset_dir.is_dir():
            raise ValueError(
                f"Dataset path '{dataset_dir}' is not a directory")

    def _collect_prompts(
        self,
        dataset_dir: Path,
        prompt_file: Path,
        instruction_file: Path,
    ) -> list[Prompt]:
        prompts = self._collect_prompts_recursive(
            current_dir=dataset_dir,
            prompt_file_name=prompt_file.name,
            instruction_file_name=instruction_file.name,
            current_instruction_path=None,
        )

        if not prompts:
            raise FileNotFoundError(
                f"No prompt files named '{prompt_file.name}' found in '{dataset_dir}'"
            )

        return prompts

    def _collect_prompts_recursive(
        self,
        current_dir: Path,
        prompt_file_name: str,
        instruction_file_name: str,
        current_instruction_path: Path | None,
    ) -> list[Prompt]:
        prompts: list[Prompt] = []

        local_instruction_path = current_dir.joinpath(instruction_file_name)
        if local_instruction_path.is_file():
            current_instruction_path = local_instruction_path

        local_prompt_path = current_dir.joinpath(prompt_file_name)

        if local_prompt_path.is_file():

            if current_instruction_path is None:
                raise FileNotFoundError(
                    f"No instruction file found for prompt '{local_prompt_path}'"
                )

            prompts.append(
                Prompt(
                    prompt_path=local_prompt_path,
                    instruction_path=current_instruction_path,
                )
            )

        for child in current_dir.iterdir():
            if child.is_dir():
                prompts.extend(
                    self._collect_prompts_recursive(
                        current_dir=child,
                        prompt_file_name=prompt_file_name,
                        instruction_file_name=instruction_file_name,
                        current_instruction_path=current_instruction_path,
                    )
                )

        return prompts

    def _get_instruction_text(
        self,
        instruction_path: Path,
        instruction_cache: dict[Path, str],
    ) -> str:
        if instruction_path not in instruction_cache:
            instruction_cache[instruction_path] = instruction_path.read_text(
                encoding="utf-8")

        return instruction_cache[instruction_path]

    def _build_response_file_path(
        self,
        timestamp: str,
        dataset_dir: Path,
        output_dir: Path,
        prompt_file: Path,
        response_file: Path,
        ai_service: AIService,
        repetition: int,
        version: int,
        is_failed: bool
    ) -> Path:
        provider = self._sanitize_file_name_part(ai_service.provider)
        model = self._sanitize_file_name_part(ai_service.model)
        failed_suffix = "_FAILED" if is_failed else ""

        relative_prompt_dir = prompt_file.parent.relative_to(dataset_dir)

        base_path = (
            output_dir
            / timestamp
            / f"{provider}_{model}"
            / relative_prompt_dir
            / f"rep_{repetition}"
        )

        base_path.mkdir(parents=True, exist_ok=True)

        return base_path.joinpath(
            f"{response_file.stem}_"
            f"v{version}"
            f"{failed_suffix}"
            f"{response_file.suffix}"
        )

    def _sanitize_file_name_part(self, value: str) -> str:
        return (
            value
            .replace("/", "-")
            .replace("\\", "-")
            .replace(":", "-")
            .replace(" ", "_")
        )

    def _get_log_messages(
        self,
        result: GenerationResult,
        service: AIService,
        prompt_path: Path,
        response_file_path: Path,
    ) -> list[str]:
        status = "FAILED" if result.is_failed else "SUCCESSFUL"

        msg = []
        msg.append(f"Generation {status}:")
        msg.append(f"{self.logger_indent}prompt: {prompt_path}")
        msg.append(f"{self.logger_indent}response: {response_file_path}")

        if result.is_failed:
            msg.append(f"{self.logger_indent}error_type: {type(result.error).__name__}")
            msg.append(f"{self.logger_indent}error_message: {str(result.error)}")

        return msg

    def strip_markdown_code_fence(self, text: str) -> str:
        text = text.strip()
        marker = "```"

        if not text.startswith(marker):
            return text

        lines = text.splitlines()

        if len(lines) < 2:
            return text

        first_line = lines[0].strip().lower()
        last_line = lines[-1].strip()

        if first_line.startswith(marker) and last_line.startswith(marker):
            return "\n".join(lines[1:-1]).strip()

        return text