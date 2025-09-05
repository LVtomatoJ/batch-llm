from app.core.config import config
from openai import AsyncOpenAI
from loguru import logger


class LLMService:

    def __init__(self, api_key: str):
        logger.info(f'Initialized LLMService with api_key: {api_key}')
        if api_key:
            logger.info(f'Using provided api_key: {api_key}')
            self.client = AsyncOpenAI(api_key=api_key)
        else:
            logger.info(f'Using default api_key: {config.openai_api_key}')
            self.client = AsyncOpenAI(api_key=config.openai_api_key)

    async def generate_response(self, question: str, model: str) -> str:
        logger.info(
            f'Generating response for question: {question} with model: {model}'
        )
        response = await self.client.chat.completions.create(model=model,
                                                             messages=[{
                                                                 "role":
                                                                 "user",
                                                                 "content":
                                                                 question
                                                             }],
                                                             stream=False)
        logger.info(f'Response: {response.choices[0].message.content}')
        return response.choices[0].message.content
