FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade && \
    apk add --no-cache \
    gcc \
    mariadb \
    mariadb-dev \
    musl-dev \
    libjpeg-turbo-dev \
    zlib-dev

COPY base/prod-entrypoint.sh /startup/
RUN chmod +x /startup/prod-entrypoint.sh
COPY base/gc.sh /etc/periodic/daily/gc
RUN chmod a+x /etc/periodic/daily/gc

WORKDIR /code
COPY base/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
