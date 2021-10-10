# Web of Web Trust - Server

The server for the web of web trust project

## Requirements

```text
golang
python3
```

optional

```text
docker
```

## Installation

The Installation instructions for the server

### ruegen-scraper

```bash
cd ruegen-scraper
pip3 install -r requirements.txt
```

### go-scraper

```bash
cd go-scraper
go install
```

Please execute the binary only in the go-scraper directory.

### backend

```bash
cd backend
pip install -r requirements.txt
python manage.py
```

or with docker

```bash
cd backend
docker-compose up
```
