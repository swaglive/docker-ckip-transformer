ARG         base=python:3.10.6-slim-buster


###

FROM        ${base} as build

WORKDIR     /usr/src/app
COPY        requirements.txt .

RUN         apt-get update && \
            apt-get install -y build-essential && \
            pip install -r requirements.txt

###

FROM        ${base}

ARG         ckip_transformer_model=bert-base

ENV         PYTHONUNBUFFERED=1
ENV         CKIP_TRANSFORMER_MODEL=${ckip_transformer_model}

EXPOSE      8000/tcp
CMD         ["uwsgi", "--ini", "config/uwsgi.ini", "--http", ":8000"]

WORKDIR     /usr/src/app


COPY        --from=build /usr/local/bin /usr/local/bin
COPY        --from=build /usr/local/lib /usr/local/lib

COPY        . .

RUN         flask shell
