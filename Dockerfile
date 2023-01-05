ARG         base=python:3.10.9-slim-buster


###

FROM        ${base} as build

WORKDIR     /usr/src/app
COPY        poetry.lock .
COPY        pyproject.toml .

RUN         apt-get update && \
            apt-get install -y \
                build-essential && \
            pip install poetry && \
            poetry install -vv -n --only=main --no-root && \
            apt-get remove build-essential

###

FROM        ${base}

ARG         model=bert-base

WORKDIR     /usr/src/app

ENV         PYTHONUNBUFFERED=1
ENV         CKIP_TRANSFORMER_MODEL=${model}

EXPOSE      8000/tcp
CMD         ["uwsgi", "--ini", "config/uwsgi.ini", "--http", ":8000"]

COPY        --from=build /usr/local /usr/local
COPY        app.py app.py

# RUN         flask shell
