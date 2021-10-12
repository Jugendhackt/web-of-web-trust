# GoLang docker image based on https://docs.docker.com/language/golang/build-images/ docker docs

FROM golang:1.16-alpine as build

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
COPY config.json /

RUN go mod download

COPY *.go ./
COPY lib/ ./lib/

RUN go build -o /docker-scraper

FROM alpine:latest

WORKDIR /

COPY --from=build /docker-scraper /docker-scraper
COPY --from=build /app/config.json /config.json

ENTRYPOINT ["./docker-scraper"]
