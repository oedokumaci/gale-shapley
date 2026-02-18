FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock* README.md ./
COPY src/ src/
COPY frontend/ frontend/
COPY config/ config/

RUN uv sync --extra cli --extra gui --no-dev

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "gale_shapley_algorithm"]
