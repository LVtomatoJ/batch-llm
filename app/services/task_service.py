import uuid
from loguru import logger
from app.services.llm_service import LLMService


class Task:

    def __init__(self, var: str, question: str, model: str,
                 llm_service: LLMService):
        logger.info(
            f'Initializing Task with var: {var}, question: {question}, model: {model}'
        )
        self.var = var
        self.question = question
        self.model = model
        self.llm_service = llm_service
        self.result = ''
        self.id = str(uuid.uuid4())
        self.status = 'pending'

    async def start_once(self):
        self.status = 'running'
        logger.info(
            f'Starting Task[{self.id}] with var: {self.var}, question: {self.question}, model: {self.model}'
        )

        self.result = await self.llm_service.generate_response(
            self.question.format(var=self.var), self.model)
        logger.info(f'Task[{self.id}] result: {self.result}')
        self.status = 'completed'
        return self.result


class TaskService:

    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks
