FROM python:3.10.0-slim-buster

COPY . /opt/app/

WORKDIR /opt/app/

RUN apt update -qqy && apt install -qqy build-essential git postgresql-client postgresql-client-common postgresql libffi-dev gcc && python3 -m pip install -r requirements.txt 

EXPOSE 8080

ENV PORT=8080

CMD ["bash", "docker.sh"]
