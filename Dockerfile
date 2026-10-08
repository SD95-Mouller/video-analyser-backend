FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	COOKIES_PATH=/app/temp/cookies.txt \
	DOWNLOAD_DIR=/app/temp \
	HF_HUB_OFFLINE=1

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt yt-dlp

COPY app ./app
COPY models /app/models
COPY cookies.txt /app/temp/cookies.txt
RUN mkdir -p /app/temp \
	&& useradd --create-home --shell /usr/sbin/nologin app \
	&& chown -R app:app /app

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]