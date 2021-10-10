FROM python:3.9.0-slim

COPY . /opt/app/

WORKDIR /opt/app/

RUN apt update -qqy && apt install -qqy build-essential git postgresql-client postgresql-client-common postgresql libffi-dev gcc && pip install poetry && python3 -m pip install -r requirements.txt

EXPOSE 8080

ENV PORT=8080

CMD ["docker.sh"]
