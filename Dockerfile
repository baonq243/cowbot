FROM python:alpine

LABEL org.opencontainers.image.source https://github.com/baonq243/cowbot

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]