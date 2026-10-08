import os
from functools import lru_cache
from pathlib import Path

from faster_whisper import WhisperModel


TEMP_DIR = Path(__file__).resolve().parents[2] / "temp"
VIDEO_EXTENSIONS = {".mp4", ".m4v", ".mov", ".mkv", ".webm", ".avi"}
AUDIO_EXTENSIONS = {".m4a", ".aac", ".mp3", ".wav", ".flac", ".ogg", ".opus"}


@lru_cache(maxsize=1)
def _get_model() -> WhisperModel:
	model_path = os.getenv("WHISPER_MODEL_PATH", "/app/models/faster-whisper-base")
	if not Path(model_path).exists():
		model_path = "base"  # 回退到自动下载/本地缓存
	return WhisperModel(model_path, device="cpu", compute_type="int8")


def _pick_best_media_file(filename: str) -> Path:
	matches = sorted(
		path for path in TEMP_DIR.glob(f"{filename}.*")
		if path.is_file() and path.name.startswith(f"{filename}.")
	)
	if not matches:
		raise FileNotFoundError(f"在 {TEMP_DIR} 中找不到音频文件：{filename}")

	# 下载只取音轨，优先选择音频文件；视频格式仅作兜底（如 bestaudio 回退到含音轨的合并格式）
	priority = {
		".m4a": 0,
		".aac": 1,
		".mp3": 2,
		".wav": 3,
		".flac": 4,
		".ogg": 5,
		".opus": 6,
		".mp4": 7,
		".m4v": 8,
		".mov": 9,
		".mkv": 10,
		".webm": 11,
		".avi": 12,
	}

	for required in (AUDIO_EXTENSIONS, VIDEO_EXTENSIONS):
		preferred = [
			path for path in matches if path.suffix.lower() in required
		]
		if preferred:
			return min(preferred, key=lambda path: (priority.get(path.suffix.lower(), 99), path.name.lower()))

	return min(matches, key=lambda path: (priority.get(path.suffix.lower(), 99), path.name.lower()))


def transcribe_video(filename: str) -> str:
	video_path = TEMP_DIR / f"{filename}"

	if not video_path.is_file():
		video_path = _pick_best_media_file(filename)

	segments, _ = _get_model().transcribe(str(video_path))
	return "".join(segment.text for segment in segments).strip()