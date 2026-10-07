from functools import lru_cache
from pathlib import Path

from faster_whisper import WhisperModel


TEMP_DIR = Path(__file__).resolve().parents[2] / "temp"
VIDEO_EXTENSIONS = {".mp4", ".m4v", ".mov", ".mkv", ".webm", ".avi"}
AUDIO_EXTENSIONS = {".m4a", ".aac", ".mp3", ".wav", ".flac", ".ogg", ".opus"}


@lru_cache(maxsize=1)
def _get_model() -> WhisperModel:
	return WhisperModel("base", device="cpu", compute_type="int8")


def _pick_best_media_file(filename: str) -> Path:
	matches = sorted(
		path for path in TEMP_DIR.glob(f"{filename}.*")
		if path.is_file() and path.name.startswith(f"{filename}.")
	)
	if not matches:
		raise FileNotFoundError(f"在 {TEMP_DIR} 中找不到视频文件：{filename}")

	priority = {
		".mp4": 0,
		".m4v": 1,
		".mov": 2,
		".mkv": 3,
		".webm": 4,
		".avi": 5,
		".m4a": 6,
		".aac": 7,
		".mp3": 8,
		".wav": 9,
		".flac": 10,
		".ogg": 11,
		".opus": 12,
	}

	for required in (VIDEO_EXTENSIONS, AUDIO_EXTENSIONS):
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