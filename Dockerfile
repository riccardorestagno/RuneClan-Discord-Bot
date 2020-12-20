# Based on Python
FROM python:alpine

LABEL Name=runeclan_discord_bot Version=0.0.1

# Our bot is in runeclanbot, so copy that whole folder over to /runeclanbot on the container filesystem
WORKDIR /runeclanbot
COPY runeclanbot .
COPY requirements.txt .

RUN apk add build-base

# Using pip:
RUN python3 -m pip install -r requirements.txt
# Start bot
CMD ["python3", "-u", "./runeclanbot.py"]