FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y gettext libpq-dev build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /code

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .
RUN chmod 755 /code/start-django.sh

EXPOSE 8000

ENTRYPOINT [ "/code/start-django.sh" ]

