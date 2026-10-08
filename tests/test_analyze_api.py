from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.transform import transcribe_video

client = TestClient(app)


def test_analyze_returns_200(monkeypatch):
    monkeypatch.setattr("app.api.v1.analyze.download_video", lambda url, filename: None)
    monkeypatch.setattr("app.api.v1.analyze.transcribe_video", lambda filename: "假的转录文本")
    monkeypatch.setattr(
        "app.api.v1.analyze.summarize_text",
        lambda text, api_key=None: "假的总结",
    )

    response = client.post(
        "/api/v1/analyze",
        json={"video_url": "https://www.bilibili.com/video/BV1xx411c7mD"},
        headers={"Authorization": "Bearer sk-test","content-type": "application/json"}
    )
    assert response.status_code == 200
    assert "summary" in response.json()["data"]


def test_transcribe_prefers_audio_file_over_video(monkeypatch, tmp_path):
    filename = "video_test"
    video_path = tmp_path / f"{filename}.mp4"
    audio_path = tmp_path / f"{filename}.m4a"
    video_path.write_bytes(b"video")
    audio_path.write_bytes(b"audio")

    monkeypatch.setattr("app.services.transform.TEMP_DIR", tmp_path)

    class FakeModel:
        def transcribe(self, path):
            assert Path(path).suffix.lower() == ".m4a"
            return ([type("Segment", (), {"text": "hello"})()], None)

    monkeypatch.setattr("app.services.transform._get_model", lambda: FakeModel())

    assert transcribe_video(filename) == "hello"