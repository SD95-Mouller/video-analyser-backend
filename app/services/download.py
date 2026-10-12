# 音频下载功能（仅下载音轨，无需 ffmpeg 合并）
from app.config import COOKIES_PATH, DOWNLOAD_DIR
import yt_dlp

def download_video(url: str, filename: str = "video"):
    if not COOKIES_PATH or not DOWNLOAD_DIR:
        raise RuntimeError("COOKIES_PATH 和 DOWNLOAD_DIR 必须在环境变量中配置")

    opts = {
        "cookiefile": COOKIES_PATH,
        "noplaylist": True,
        "format": "bestaudio/best",
        "paths": {"home": DOWNLOAD_DIR},
        "outtmpl": f"{filename}.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as exc:
        raise RuntimeError(f"视频下载失败：{exc}") from exc