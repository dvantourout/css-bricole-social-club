FROM python:3.13-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:python3.13-alpine /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/

# Copy the application into the container.
COPY ./backend /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE 5000