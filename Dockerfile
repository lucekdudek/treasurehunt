FROM python:3.9.6-buster as builder

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv  \
 && pipenv lock -r > requirements.txt

RUN apt-get -y update \
 && apt-get -y upgrade \
 && pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.9.6-slim-buster

COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /app

WORKDIR /app
