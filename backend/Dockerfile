FROM python:3.9-alpine as base

FROM base as builder

RUN apk add --no-cache gcc git musl-dev libffi-dev openssl-dev make postgresql-dev

RUN pip install poetry

ADD . /src/

WORKDIR /src

RUN python -m venv /env && . /env/bin/activate && poetry install

FROM base

RUN apk add --no-cache postgresql-libs

COPY --from=builder /env /env
COPY --from=builder /src /src

WORKDIR /src

CMD ["sh", "docker.sh"]
