import os
from openai import OpenAI

SYSTEM_PROMPT = """You are a function calling assistant.

Return ONLY valid JSON in this format:
[{"name": "function_name", "arguments": {"arg1": "value"}}]

Rules:
- No explanations
- No extra text
- Only JSON array
"""

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

MODEL = os.getenv("LLM_MODEL_ID", "deepseek-chat")


def call_llm(query: str):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        temperature=0
    )
    return resp.choices[0].message.content


class MyAgent:
    def run(self, query: str):
        return call_llm(query)