from openai import AsyncOpenAI

class OpenAIService():
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_response(self, prompt: str) -> str:
        response = await self.client.responses.create(
            model="gpt-5.4-mini",
            instructions="You are a coding assistant that talks like a pirate.",
            input=prompt,
        )
        return response.output_text