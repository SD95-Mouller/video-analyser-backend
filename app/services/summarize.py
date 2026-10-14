# ai总结功能
from openai import OpenAI

def summarize_text(text: str, api_key: str | None = None) -> str:
	if not text.strip():
		return ""

	key = api_key
	if not key:
		raise ValueError("未配置 DEEPSEEK_API_KEY")

	client = OpenAI(
		api_key=key,
		base_url="https://api.deepseek.com",
	)
	response = client.chat.completions.create(
		model="deepseek-chat",
		messages=[
			{
				"role": "system",
				"content": "这是一段视频中的文字内容，请用中文准确、简洁地总结视频中的内容，保留核心观点和重要信息，不要使用md格式。",
			},
			{"role": "user", "content": text},
		],
	)

	summary = response.choices[0].message.content
	if not summary:
		raise RuntimeError("AI 未返回总结内容")
	return summary.strip()