from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from config import Config, Dataset
from openai_service import OpenAIService


@dataclass(frozen=True)
class Prompt:
    prompt_path: Path
    instruction_path: Path


class Runner:
    def __init__(self, config: Config):
        self._config = config

    async def run(self) -> None:
        dataset = self._config.dataset
        self._validate_dataset_dir(dataset.dir_path)

        prompts = self._collect_prompts(
            dataset_dir=dataset.dir_path,
            prompt_file=dataset.prompt_file,
            instruction_file=dataset.instruction_file,
        )

        openai_service = OpenAIService(
            api_key=self._config.credentials.openai.api_key)

        instruction_cache: dict[Path, str] = {}

        for prompt in prompts:
            instructions = self._get_instruction_text(
                instruction_path=prompt.instruction_path, instruction_cache=instruction_cache)
            
            response = await self.generate_response(dataset, openai_service, instructions, prompt)

            self._write_response(
                prompt=prompt, response=response, response_file=dataset.response_file)

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

    async def generate_response(self, dataset: Dataset, ai_service: OpenAIService, instructions: str, prompt: Prompt):
        prompt_text = prompt.prompt_path.read_text(encoding="utf-8")

        response = await ai_service.generate_response(
            instructions=instructions,
            prompt=prompt_text,
        )

        print(f"Generated response for: {prompt.prompt_path}")
        print("-" * 80)

        return response

    def _write_response(
        self,
        prompt: Prompt,
        response: str,
        response_file: Path,
    ) -> None:
        response_path = prompt.prompt_path.parent.joinpath(response_file.name)
        response_path.write_text(response, encoding="utf-8")
