FROM python:3.11.3-slim-bullseye AS base

WORKDIR /app

RUN set -ex; \
    \
    apt-get update; \
    apt-get upgrade; \
    apt-get clean; \
    \
    rm -rf /var/lib/apt/lists/*

FROM base AS build
COPY ./requirements/ ./requirements/
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
#ENV DJANGO_SETTINGS_MODULE settings.production
# RUN python3 manage.py migrate --no-input && python3 manage.py loaddata /app/orders/fixtures/Products.json  && python3 manage.py collectstatic --no-input
RUN rm -rf .env*

FROM base AS prod
COPY --from=build /app /app
COPY --from=build /usr/local /usr/local
CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info", "timecashier.wsgi:application"]
