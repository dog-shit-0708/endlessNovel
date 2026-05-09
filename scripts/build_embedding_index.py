"""
构建 chapter_embeddings 向量索引
- 解析 all_summaries.md → 按章节分块
- 调用 doubao-embedding API 生成 embedding（1024维）
- 存入 FAISS（持久化到 data/fanfic_library/faiss_index/）
"""
import sys
import os
import re
import json
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.embedding_utils import get_embedding, EMBEDDING_DIM

# 加载 .env 获取 ARK_API_KEY
load_dotenv()

# === 路径配置 ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SUMMARIES_PATH = PROJECT_ROOT / "data" / "fanfic_library" / "all_summaries.md"
FAISS_DIR = PROJECT_ROOT / "data" / "fanfic_library" / "faiss_index"
TXT_DIR = PROJECT_ROOT / "data" / "fanfic_library" / "txt"

# 尝试导入 FAISS
try:
    import faiss
except ImportError:
    print("[build_embedding_index] 错误: 请先安装 FAISS: pip install faiss-cpu")
    raise


def parse_summaries(filepath: str) -> list[dict]:
    """解析 all_summaries.md，返回 [{chapter_num, summary}, ...]"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 按 ## 第X章 分割
    pattern = r"^## 第(\d+)章$"
    lines = content.split("\n")
    
    chapters = []
    current_chapter = None
    current_lines = []

    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            if current_chapter is not None:
                chapters.append({
                    "chapter_num": current_chapter,
                    "summary": "\n".join(current_lines).strip()
                })
            current_chapter = int(match.group(1))
            current_lines = []
        elif current_chapter is not None:
            # 跳过分隔线
            if line.strip().startswith("---") or line.strip().startswith("==="):
                continue
            current_lines.append(line)

    # 最后一章
    if current_chapter is not None:
        chapters.append({
            "chapter_num": current_chapter,
            "summary": "\n".join(current_lines).strip()
        })

    return chapters


def main():
    print(f"[build_embedding_index] 解析摘要文件: {SUMMARIES_PATH}")
    chapters = parse_summaries(str(SUMMARIES_PATH))
    print(f"[build_embedding_index] 共解析到 {len(chapters)} 章")

    # 创建 FAISS 索引（余弦相似度用 Inner Product + 归一化）
    # IndexFlatIP = Inner Product，余弦相似度需要先归一化向量
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    
    metadata_list = []
    embeddings_list = []

    for ch in chapters:
        chapter_num = ch["chapter_num"]
        summary = ch["summary"]
        print(f"[build_embedding_index] 第{chapter_num}章 embedding...", end=" ", flush=True)

        emb = get_embedding(summary)
        embeddings_list.append(emb)
        metadata_list.append({
            "id": f"chapter_{chapter_num}",
            "chapter_num": chapter_num,
            "txt_file": f"chapter{chapter_num}.txt",
            "summary": summary
        })
        print("done")

    # 转换为 numpy 数组并归一化（用于余弦相似度）
    embeddings_np = np.array(embeddings_list, dtype=np.float32)
    faiss.normalize_L2(embeddings_np)  # L2 归一化后，IP = 余弦相似度
    
    # 添加到索引
    index.add(embeddings_np)
    print(f"[build_embedding_index] 已添加 {index.ntotal} 条向量到 FAISS 索引")

    # 保存索引文件（FAISS 不支持中文路径，先用英文临时路径）
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[build_embedding_index] 创建目录: {FAISS_DIR}")
    
    # 使用临时英文路径保存
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_index_path = Path(tmpdir) / "index.faiss"
        print(f"[build_embedding_index] 临时保存到: {tmp_index_path}")
        faiss.write_index(index, str(tmp_index_path))
        
        # 移动到最终位置
        index_path = FAISS_DIR / "chapter_index.faiss"
        shutil.copy(str(tmp_index_path), str(index_path))
        print(f"[build_embedding_index] 索引已复制到: {index_path}")
    
    # 保存元数据
    metadata_path = FAISS_DIR / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)

    print(f"\n[build_embedding_index] 完成！共写入 {len(metadata_list)} 条向量")
    print(f"[build_embedding_index] FAISS 索引: {index_path}")
    print(f"[build_embedding_index] 元数据: {metadata_path}")
    print(f"[build_embedding_index] 维度: {EMBEDDING_DIM}")


if __name__ == "__main__":
    main()
