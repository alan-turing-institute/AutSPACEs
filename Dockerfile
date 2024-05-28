ARG PYTHON_VERSION=3.12.2-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TINI_VERSION=v0.19.0
ENV DJANGO_ENV=production

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    wget \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Installing `tini` utility:
# https://github.com/krallin/tini

RUN wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
    && chmod +x /usr/local/bin/tini && tini --version

RUN mkdir -p /code

WORKDIR /code

RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction
COPY . /code

EXPOSE 8000

# load entrypoint script for launching guincorn
COPY ./docker/django/gunicorn.sh /docker-entrypoint.sh

# Setting up proper permissions:
RUN chmod +x '/docker-entrypoint.sh' \
    && groupadd -r web && useradd -d /code -r -g web web \
    && chown web:web -R /code \
    && mkdir -p /var/www/django/static /var/www/django/media \
    && chown web:web /var/www/django/static /var/www/django/media

USER web

# CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "server.wsgi"]
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]
