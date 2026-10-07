FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	COOKIES_PATH=/run/secrets/cookies.txt \
	DOWNLOAD_DIR=/app/temp
# cookies.txt 是敏感文件，包含用于身份验证下载的 cookie。
# 它应该在 docker run 时挂载。

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt yt-dlp

COPY app ./app
RUN mkdir -p /app/temp \
	&& useradd --create-home --shell /usr/sbin/nologin app \
	&& chown -R app:app /app

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]