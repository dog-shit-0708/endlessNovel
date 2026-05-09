"""Embedding 工具函数"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ARK_API_KEY = os.getenv("ARK_API_KEY")
EMBEDDING_URL = "https://ark.cn-beijing.volces.com/api/v3/embeddings/multimodal"
EMBEDDING_MODEL = "ep-20260331172640-n6p74"
EMBEDDING_DIM = 1024


def get_embedding(text: str) -> list[float]:
    """调用 doubao-embedding API"""
    print(f"[get_embedding] 请求 embedding，文本长度: {len(text)} 字符")
    print(f"[get_embedding] API Key 是否存在: {bool(ARK_API_KEY)}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ARK_API_KEY}"
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": [{"type": "text", "text": text}],
        "dimensions": EMBEDDING_DIM
    }
 
    resp = requests.post(EMBEDDING_URL, headers=headers, json=payload, timeout=30)
 
    resp.raise_for_status()
    data = resp.json()
    if "data" not in data:
        raise ValueError(f"API返回不包含'data'字段: {list(data.keys())}")
    if "embedding" in data["data"]:
        print(f"[get_embedding] 成功获取 embedding，维度: {len(data['data']['embedding'])}")
        return data["data"]["embedding"]
    else:
        raise ValueError(f"data字段中未找到embedding: {list(data['data'].keys())}")
