from .base import AIService
from config import AIConfig
from .google_ai_service import GoogleAIService
from .openai_service import OpenAIService


class AIServiceFactory:
    @staticmethod
    def create_services(config: AIConfig) -> list[AIService]:
        services: list[AIService] = []

        for provider in config.providers:
            match provider.name:
                case "openai":
                    services.append(
                        OpenAIService(
                            api_key=provider.api_key,
                            model=provider.model,
                            temperature=provider.temperature,
                        )
                    )

                case "google":
                    services.append(
                        GoogleAIService(
                            api_key=provider.api_key,
                            model=provider.model,
                            temperature=provider.temperature,
                        )
                    )

                case _:
                    raise ValueError(
                        f"Unsupported AI provider: {provider.name}")

        return services
