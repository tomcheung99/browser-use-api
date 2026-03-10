from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.schemas import TaskRequest, TaskResponse
from app.agent import run_browser_task

router = APIRouter()
security = HTTPBearer(auto_error=False)


def verify_api_key(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
    """Optional bearer token auth — only enforced when API_SECRET_KEY is set."""
    if settings.api_secret_key:
        if credentials is None or credentials.credentials != settings.api_secret_key:
            raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/run", response_model=TaskResponse, dependencies=[Depends(verify_api_key)])
async def run_task(request: TaskRequest):
    """Run a browser automation task and return the result."""
    try:
        result = await run_browser_task(
            task=request.task,
            llm_provider=request.llm_provider or settings.default_llm_provider,
            model=request.model or settings.default_model,
            max_steps=request.max_steps,
        )
        return TaskResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
