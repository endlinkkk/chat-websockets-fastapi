FROM python:3.12.4-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /project


COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config --local virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /project/
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh