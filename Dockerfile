# syntax=docker/dockerfile:1.6
FROM python:3.13-slim AS base

FROM base AS builder

# Install uv
RUN pip install uv

WORKDIR /app
COPY uv.lock pyproject.toml /app/

# Install uv and dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM base
COPY --from=builder /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
EXPOSE 8050
CMD ["python", "app.py"]
