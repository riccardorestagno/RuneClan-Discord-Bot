# Based on Python
FROM python:alpine

LABEL Name=runeclan_discord_bot Version=0.0.1

# Our bot is in app, so copy that whole folder over to /app on the container filesystem
WORKDIR /app
COPY app .

RUN apk add build-base

# Using pip:
RUN python3 -m pip install -r requirements.txt
# Start bot
CMD ["python3", "-u", "./runeclanbot.py"]