FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip \
    && pip install poetry gunicorn \
    && poetry config virtualenvs.create false \
    && poetry install --without dev

COPY . /app/

CMD ["gunicorn", "quotes.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
