FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv --no-cache-dir

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ ./src/
COPY embed/ ./embed/
COPY main.py ./

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "main.py", "--serve"]
