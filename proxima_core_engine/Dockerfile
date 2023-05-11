# BUILDER
FROM python:3.9.6-alpine3.14 as builder
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install flake8==3.9.2
COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# FINAL
FROM python:3.9.6-alpine3.14
RUN set -eux && \
    addgroup -S app && \
    adduser -S app -G app && \
    apk update && \
    apk add --no-cache libpq && \
    mkdir -p /home/app/web/staticfiles /home/app/web/mediafiles
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache /wheels/* && \
    rm -rf /wheels && \
    chown -R app:app $APP_HOME && \
    rm -f requirements.txt
COPY . $APP_HOME
USER app

