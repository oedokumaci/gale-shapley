FROM node:20-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM python:3.13-slim
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock* README.md ./
COPY src/ src/
COPY config/ config/
COPY --from=frontend /app/frontend/dist frontend/dist

RUN uv sync --extra cli --extra gui --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "gale_shapley_algorithm._api.app:app", "--host", "0.0.0.0", "--port", "8000"]
