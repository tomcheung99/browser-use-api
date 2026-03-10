from pydantic import BaseModel


class TaskRequest(BaseModel):
    task: str
    llm_provider: str | None = None  # "openai" | "anthropic"
    model: str | None = None
    max_steps: int = 50


class TaskResponse(BaseModel):
    success: bool
    result: str | None = None
