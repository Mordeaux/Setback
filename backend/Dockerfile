########################################
# BASE
########################################
FROM python:latest AS base

LABEL authors="Michael Mordowanec"

RUN \
    apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    libpq-dev \
    python3-dev \
    libpcre3 \
    libpcre3-dev \
    python-mysqldb \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

WORKDIR /usr/src/app

COPY pyproject.toml .
#COPY poetry.lock .
COPY manage.py .
COPY backend/ .

RUN poetry install

########################################
# Development
########################################
FROM base AS development

ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver"]

########################################
# TESTS
########################################
FROM base AS test

WORKDIR /home/setback

ENTRYPOINT [ "poetry", "run", "tox" ]

########################################
# RELEASE
########################################
FROM base AS release

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver"]
