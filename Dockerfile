FROM python:3.12-slim

WORKDIR /usr/src/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . .

RUN uv sync --extra test

ENV number_of_simulations=1

CMD ["uv", "run", "python", "-m", "gale_shapley"]
