FROM python:3.9-alpine3.13
LABEL maintainer="jakeoliverlee"

ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app

EXPOSE 8000



ARG DEV=false
RUN pip install flake8
# Establishes virtual env inside the docker image, installs requirements, removes tmp directory, add a new user which isn't the root user.
RUN python -m venv /py && \
/py/bin/pip install --upgrade pip && \
# Install postgresql client package
apk add --update --no-cache postgresql-client && \
# Groups the packages into tmp-build-deps
apk add --update --no-cache --virtual .tmp-build-deps \
    # Listed packages needed to be installed.
    build-base postgresql-dev musl-dev && \
/py/bin/pip install -r /tmp/requirements.txt && \
# If DEV environment variable = true, install dev dependencies.
if [ $DEV = "true"]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
fi && \
rm -rf /tmp && \
# Removes packages that are now no longer needed since they are only needed for installing psycopg2
apk del .tmp-build-deps && \
adduser \
    --disabled-password \
    --no-create-home \
    django-user

    


ENV PATH="/py/bin:$PATH"

USER django-user
