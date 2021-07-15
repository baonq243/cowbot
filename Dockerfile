FROM python:3.9.6-slim-buster

LABEL org.opencontainers.image.source https://github.com/baonq243/cowbot

RUN mkdir /app

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y \
  iputils-ping \
  dnsutils \
  nmap \
  mtr \
  traceroute \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]