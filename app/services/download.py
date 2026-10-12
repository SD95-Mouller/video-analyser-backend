# 音频下载功能（仅下载音轨，无需 ffmpeg 合并）
import subprocess
import os
from app.config import COOKIES_PATH, DOWNLOAD_DIR


def download_video(url: str, filename: str = "video"):
    """仅下载音轨，用于语音转录。不下载视频流，速度更快且容器无需 ffmpeg。"""
    if not COOKIES_PATH or not DOWNLOAD_DIR:
        raise RuntimeError("COOKIES_PATH 和 DOWNLOAD_DIR 必须在环境变量中配置")

    # 给 yt-dlp 子进程准备一个明确 UTF-8 的环境
    child_env = os.environ.copy()
    child_env["LANG"] = "C.UTF-8"
    child_env["LC_ALL"] = "C.UTF-8"
    child_env["PYTHONIOENCODING"] = "utf-8"

    try:
        subprocess.run(
            [
                "yt-dlp",
                "--cookies",
                COOKIES_PATH,
                "--no-playlist",
                "--format",
                "bestaudio/best",
                "-P",
                DOWNLOAD_DIR,
                "-o",
                f"{filename}.%(ext)s",
                url,
            ],
            check=True,
            encoding="utf-8",       # 新增：明确用 utf-8
            errors="replace",       # 新增：遇到无法解码的字符就替换，不抛错
            capture_output=True,
            text=True,
            env=child_env,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("找不到 yt-dlp，请确认已安装并且命令在 PATH 中") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "没有提供错误详情")
        if isinstance(detail, bytes):
            detail = detail.decode("utf-8", errors="replace")
        detail = detail.strip()
        raise RuntimeError(f"视频下载失败：{detail}") from exc