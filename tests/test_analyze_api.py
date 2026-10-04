from fastapi.testclient import TestClient
from app.main import app

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