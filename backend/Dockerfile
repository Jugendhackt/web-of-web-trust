FROM python:3.10.0-slim-buster

COPY . /opt/app

WORKDIR /opt/app/

RUN apt update && apt install -yqq build-essential libffi-dev gcc && python3 -m pip install poetry && poetry install

CMD ["poetry", "run" "python3", "manage.py"]
