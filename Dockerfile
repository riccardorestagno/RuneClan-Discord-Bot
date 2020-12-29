# Multi-stage build to reduce image size
# https://snorfalorpagus.net/blog/2019/07/30/multi-stage-docker-builds-for-python-apps/

FROM python:alpine AS compile-image

WORKDIR /opt/runeclanbot

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

COPY requirements.txt /opt/runeclanbot/
RUN apk add build-base
RUN python3 -m pip install -r requirements.txt


FROM python:alpine AS build-image

COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

COPY runeclanbot /opt/runeclanbot/
WORKDIR /opt/runeclanbot
# Start bot
CMD ["python3", "-u", "./runeclanbot.py"]