###########
# BUILDER #
###########

# pull official base image
FROM python:3.10.7-slim-buster as builder

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential

# lint
RUN python -m pip install -U pip
RUN pip install --upgrade pip
RUN apt-get -y update
RUN apt-get -y install git
RUN pip install ez_setup 
RUN pip install flake8==5.0.4
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu --no-cache-dir
RUN pip install git+https://github.com/Proximaagent/proxima-kafka-connect-api.git

COPY . .
# RUN flake8 --ignore=E50RUN1,F401 .
# install python dependencies
# COPY ./requirements.txt .
#
# RUN python3 -m nltk.downloader punkt
# RUN python3 -m nltk.downloader wordnet

# RUN chmod -R +rwx /usr/src/nltk_data
# RUN chmod -R +rwx /use/src/root/nltk_data
# RUN chmod +rwx /usr/src/nltk_data/corpora/cmudict.zip
RUN  pip install fairseq
COPY ./local_dev_packages /code/local_dev_packages
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.10.7-slim-buster

# create directory for the app user
# RUN mkdir -p /home/app

# create the app user
# RUN addgroup --system app && adduser --system --group app

# create the appropriate directories

WORKDIR /code

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat build-essential
# RUN apt-get update && apt-get install -y --no-install-recommends netcat build-essential
RUN pip install ez_setup 
RUN python -m pip install -U pip
RUN pip install --upgrade pip
RUN apt-get -y update
RUN apt-get -y install git
COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt .
COPY --from=builder /code/private-local.txt .
COPY --from=builder /code/local_dev_packages/ibl-kafka-connect-api .


RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*
# RUN pip install -r private-local.txt
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu --no-cache-dir
RUN pip install git+https://github.com/Proximaagent/proxima-kafka-connect-api.git

RUN  pip install fairseq

# RUN touch ./private-local-dev.txt
# RUN pip install -r ./private-local-dev.txt

# copy project
COPY . .

# chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# change to the app user
USER root

# run entrypoint.prod.sh
