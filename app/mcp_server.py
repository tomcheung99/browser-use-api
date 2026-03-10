from mcp.server.fastmcp import FastMCP

from app.config import settings

mcp = FastMCP(
    name="browser-use",
    instructions=(
        "Browser automation tool. Use run_browser_task to control a real web browser "
        "and perform tasks like searching, form filling, data extraction, and navigation."
    ),
)


@mcp.tool()
async def run_browser_task(
    task: str,
    llm_provider: str = "",
    model: str = "",
    max_steps: int = 50,
) -> str:
    """
    Run an autonomous browser automation task.

    Args:
        task: Natural language description of what to do in the browser.
              E.g. "Search Google for Python tutorials and return the top 3 links"
        llm_provider: LLM provider to use: "openai", "anthropic", or "kimi".
                      Defaults to the server's DEFAULT_LLM_PROVIDER setting.
        model: Model name. Defaults to DEFAULT_MODEL setting.
               For Kimi use "kimi-for-coding", for OpenAI use "gpt-4o".
        max_steps: Maximum number of browser actions before stopping (default: 50).

    Returns:
        The final result or extracted information from the browser task.
    """
    from app.agent import run_browser_task as _run

    return await _run(
        task=task,
        llm_provider=llm_provider or settings.default_llm_provider,
        model=model or settings.default_model,
        max_steps=max_steps,
    )
