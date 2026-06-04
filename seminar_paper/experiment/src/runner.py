from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from config import Config
from ai_services import AIServiceFactory, AIService, GenerationResult
from datetime import datetime
import shutil
from compile_handlers import CompileHandlerFactory

from logger import get_logger
logger = get_logger(__name__)


@dataclass(frozen=True)
class Prompt:
    prompt_path: Path
    instruction_path: Path


class Runner:
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

        for prompt in prompts:
            prompt_text = prompt.prompt_path.read_text(encoding="utf-8")

            instructions = self._get_instruction_text(
                instruction_path=prompt.instruction_path, instruction_cache=instruction_cache)

            for repetition in range(1, dataset.repetitions + 1):
                for service in services:
                    state_ids = set()
                    current_state_id = None

                    for version in range(1, dataset.max_versions + 1):
                        result = await service.generate_response(instructions, prompt_text, current_state_id)
                        response_file_path = self._build_response_file_path(
                            current_timestamp,
                            dataset.dir_path,
                            dataset.output_dir,
                            prompt.prompt_path,
                            dataset.response_file,
                            service,
                            repetition,
                            version,
                            result.is_failed
                        )
                        
                        state_ids.add(result.state_id)
                        current_state_id = result.state_id

                        messages = self._get_log_messages(
                            result, service, prompt.prompt_path, response_file_path)
                        log_message = " | ".join(messages)

                        if result.is_failed:
                            result.content = "\n".join(messages)
                            logger.error(log_message)
                        else:
                            logger.info(log_message)

                        # Compile code
                        compilation_result = await compile_handler.compile(result.content)

                        response_file_content = f"{result.content}\n\n{compile_handler.comment_symbol}Compilation:\n{compile_handler.comment_symbol}{compilation_result.message}"
                        response_file_path.write_text(
                            response_file_content, encoding="utf-8")

                        if not compilation_result.is_failed:
                            break

                        logger.info(
                            "Generating new prompt due to compilation failure...")
                        logger.info(
                            f"Compilation error: {compilation_result.message}")

                        prompt_text = f"Compilation failed with the following error:\n{compilation_result.message}\n\nPlease fix the code and try again."

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
            / relative_prompt_dir
            / f"{provider}_{model}"
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
        msg.append(f"Generation {status}")
        msg.append(f"provider: {service.provider}")
        msg.append(f"model: {service.model}")
        msg.append(f"prompt: {prompt_path}")
        msg.append(f"response: {response_file_path}")

        if result.is_failed:
            msg.append(f"error_type: {type(result.error).__name__}")

        return msg
