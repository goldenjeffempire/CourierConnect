FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

FROM base as builder

COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM base as production

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 5000

CMD ["daphne", "-b", "0.0.0.0", "-p", "5000", "courier.asgi:application"]
