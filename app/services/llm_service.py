from app.core.config import config
from openai import AsyncOpenAI
from loguru import logger


class LLMService:

    def __init__(self, api_key: str, tools: list[str]):
        logger.info(f'Initialized LLMService with api_key: {api_key}')
        if api_key:
            logger.info(f'Using provided api_key: {api_key}')
            self.client = AsyncOpenAI(api_key=api_key)
        else:
            logger.info(f'Using default api_key: {config.openai_api_key}')
            self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.tools = [{'type': tool} for tool in tools]
        logger.info(f'Tools: {self.tools}')

    async def generate_response(self, question: str, model: str) -> str:
        logger.info(
            f'Generating response for question: {question} with model: {model}'
        )
        response = await self.client.responses.create(model=model,
                                                      input=question,
                                                      stream=False,
                                                      tools=self.tools,
                                                      tool_choice='auto')
        logger.info(f'Response: {response.output_text}')
        return response.output_text
