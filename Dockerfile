# Standard OCI Metadata
#LABEL org.opencontainers.image.title="Penny Investment Alerts Service"
#LABEL org.opencontainers.image.description="Executes daily via cron for Penny"
#LABEL org.opencontainers.image.authors="Dominic Couture"

#FROM ubuntu:22.04
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install what we need: Python, pip, git (to fetch the code), cron
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    cron

WORKDIR /opt/penny

# latest commit on that branch. This is the ONLY clone that happens.
RUN git clone --depth 1 -b main https://github.com/mastermind-mayhem/penny.git . \
    && rm -rf .git \
    && pip3 install --upgrade pip setuptools wheel
# Install Python dependencies
RUN pip3 install -r requirements.txt

CMD ["python", "-u", "/opt/penny/src/use.py"]