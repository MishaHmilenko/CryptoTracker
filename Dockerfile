FROM python:3.10-slim as build_app

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install


COPY . /app

EXPOSE 8000

CMD ["uvicorn", "src.api.main:build_app", "--reload", "--host", "0.0.0.0"]


FROM build_app as test

RUN poetry install --with dev

