# ###########
# # BUILDER #
# ###########

# # pull official base image
# FROM python:3.9.6-alpine as builder

# # set work directory
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install psycopg2 dependencies
# RUN apk update \ && apk upgrade \
#     && apk add python3 py3-pip postgresql-dev gcc python3-dev musl-dev libc-dev libffi-dev py3-setuptools llvm-dev 
# RUN apk update && apk add --no-cache git ca-certificates
# RUN apk update && apk add --no-cache \
#     build-base \
#     freetype-dev \
#     jpeg-dev \
#     openjpeg-dev \
#     zlib-dev

# RUN pip install --no-cache-dir --upgrade setuptools
# # RUN pip wheel --wheel-dir=/usr/src/app/wheels wheel


# # lint
# RUN pip install --upgrade pip
# RUN pip install flake8==3.9.2
# COPY . .
# #RUN flake8 --ignore=E501,F401 .

# # install dependencies
# COPY ./requirements.txt .
# # generate wheels
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
# RUN pip3 install numpy
# # RUN pip install git+https://github.com/openai/whisper.git
# # install from wheels
# RUN pip wheel --wheel-dir=/usr/src/app/wheels setuptools
# RUN pip install --no-cache-dir --no-index --find-links /usr/src/app/wheels -r requirements.txt


# #########
# # FINAL #
# #########

# # pull official base image
# FROM python:3.9.6-alpine

# # create directory for the app user
# RUN mkdir -p /home/app

# # create the app user
# RUN addgroup -S app && adduser -S app -G app

# # create the appropriate directories
# ENV HOME=/home/app
# ENV APP_HOME=/home/app/web
# RUN mkdir $APP_HOME
# RUN mkdir $APP_HOME/staticfiles
# RUN mkdir $APP_HOME/mediafiles
# WORKDIR $APP_HOME

# # install dependencies
# RUN apk update \ && apk upgrade \
#     && apk add python3 py3-pip postgresql-dev gcc python3-dev musl-dev libc-dev libffi-dev py3-setuptools llvm-dev 

# RUN apk update && apk add --no-cache git ca-certificates
# RUN pip install --no-cache-dir --upgrade setuptools

# # RUN pip install git+https://github.com/openai/whisper.git
# COPY --from=builder /usr/src/app/wheels /wheels
# COPY --from=builder /usr/src/app/requirements.txt .
# RUN pip install --upgrade pip
# RUN pip3 install numpy
# RUN pip wheel --wheel-dir=/usr/src/app/wheels setuptools
# RUN pip install --no-cache /wheels/*

# # copy entrypoint.prod.sh
# # COPY ./entrypoint.prod.sh .
# # RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
# # RUN chmod +x  $APP_HOME/entrypoint.sh

# # copy project
# COPY . $APP_HOME

# # chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# # change to the app user
# USER app

# # # run entrypoint.prod.sh
# # # ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]

FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 8000

WORKDIR  /app

COPY . .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt || true
RUN pip install -r requirements.txt || true

CMD gunicorn proxima_core_engine.wsgi:application --bind 0.0.0.0:8000
