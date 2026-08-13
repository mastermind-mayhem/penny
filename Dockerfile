FROM python:3.12-slim

LABEL org.opencontainers.image.title="Penny Investment Alerts Service" \
    org.opencontainers.image.description="Runs scheduled Penny investment alerts"

ENV TZ=America/New_York \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
    && ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime \
    && printf '%s\n' "$TZ" > /etc/timezone \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system penny \
    && adduser --system --ingroup penny --home /opt/penny penny

WORKDIR /opt/penny

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=penny:penny src ./src

USER penny

CMD ["python", "-u", "src/use.py"]
