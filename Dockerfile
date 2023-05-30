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
COPY base/flushExpiredTokens /etc/periodic/daily/flushExpiredTokens
RUN chmod a+x /etc/periodic/daily/flushExpiredTokens

WORKDIR /code
COPY base/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
