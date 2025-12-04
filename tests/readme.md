# syntax=docker/dockerfile:1

##########################################
# Stage 1: Builder - Install dependencies
##########################################
FROM python:3.10-slim AS builder

# Copy uv binary from official distroless image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1

# Use copy mode for cache mounts (required for Docker)
ENV UV_LINK_MODE=copy

# Install dependencies first (better layer caching)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Then copy source code and install the project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

##########################################
# Stage 2: Runtime - Lean production image
##########################################
FROM python:3.10-slim

WORKDIR /app

# Copy only the virtualenv from builder (not uv or build tools)
COPY --from=builder /app/.venv /app/.venv

# Copy application source code
COPY --from=builder /app /app

# Activate the virtualenv by adding it to PATH
ENV PATH="/app/.venv/bin:${PATH}"

# Ensure Python outputs everything immediately (useful for logging)
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Use the virtualenv's Python explicitly
CMD ["/app/.venv/bin/python", "-m", "api.main"]
