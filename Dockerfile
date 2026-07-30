FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        freetds-dev \
        freetds-bin \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . .

EXPOSE 9090

CMD ["gunicorn", \
     "-w", "4", \
     "-b", "0.0.0.0:9090", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "Main:app"]
