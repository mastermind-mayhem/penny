# Standard OCI Metadata
#LABEL org.opencontainers.image.title="Penny Investment Alerts Service"
#LABEL org.opencontainers.image.description="Executes daily via cron for Penny"
#LABEL org.opencontainers.image.authors="Dominic Couture"

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install what we need: Python, pip, git (to fetch the code), cron
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    cron

WORKDIR /opt/penny

# latest commit on that branch. This is the ONLY clone that happens.
RUN git clone --depth 1 -b main https://github.com/mastermind-mayhem/penny.git . \
    && rm -rf .git

# Install Python dependencies
RUN pip3 install -r requirements.txt

RUN echo "00 12 * * * python3 /opt/penny/src/use.py >> /var/log/cron.log 2>&1" > /etc/cron.d/penny-cron
RUN chmod 0644 /etc/cron.d/penny-cron
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log