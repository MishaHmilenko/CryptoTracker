# Base stage
FROM python:3.10-slim as base

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY . /app

# Production stage
FROM base as build_app

CMD ["uvicorn", "src.api.main:build_app", "--reload", "--host", "0.0.0.0"]

# Test stage
FROM base as test

RUN poetry install --with dev

CMD ["pytest"]