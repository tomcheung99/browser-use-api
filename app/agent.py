from browser_use import Agent
from browser_use.browser import BrowserSession

from app.config import settings


def _build_llm(provider: str, model: str):
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model,
            anthropic_api_key=settings.anthropic_api_key,
        )
    if provider == "kimi":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model or "kimi-for-coding",
            openai_api_key=settings.kimi_api_key,
            openai_api_base="https://api.kimi.com/coding/v1",
        )
    # Default: OpenAI
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=model,
        openai_api_key=settings.openai_api_key,
    )


async def run_browser_task(
    task: str,
    llm_provider: str,
    model: str,
    max_steps: int = 50,
) -> str:
    llm = _build_llm(llm_provider, model)

    browser_session = BrowserSession(
        headless=settings.headless,
        # Needed for Docker/Railway
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
    )

    agent = Agent(
        task=task,
        llm=llm,
        browser_session=browser_session,
        max_failures=3,
    )

    try:
        history = await agent.run(max_steps=max_steps)
        # Return the final result from the agent's history
        return history.final_result() or "Task completed with no final result."
    finally:
        await browser_session.stop()
