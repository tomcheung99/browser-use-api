FROM python:3.11-slim

# Install minimal system packages (playwright --with-deps handles the rest)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install Python dependencies first (cached layer, before copying app code)
COPY pyproject.toml ./
RUN uv pip install --system --no-cache \
    "browser-use>=0.12.0" \
    playwright \
    fastapi \
    "uvicorn[standard]" \
    python-dotenv \
    "pydantic>=2.0.0" \
    pydantic-settings \
    langchain-openai \
    langchain-anthropic

# Install Playwright Chromium + all required system dependencies
RUN /usr/local/bin/playwright install chromium --with-deps

# Copy application code
COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
