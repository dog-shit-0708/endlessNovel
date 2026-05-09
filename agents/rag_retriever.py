"""
RAG 检索器 - 使用 FAISS 进行向量检索
"""
import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict

# 尝试导入 FAISS
try:
    import faiss
except ImportError:
    print("[rag_retriever] 错误: 请先安装 FAISS: pip install faiss-cpu")
    raise

from agents.embedding_utils import get_embedding, EMBEDDING_DIM

# === 路径配置 ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FAISS_DIR = PROJECT_ROOT / "data" / "fanfic_library" / "faiss_index"
DATA_DIR = PROJECT_ROOT / "data" / "fanfic_library" / "txt"
INDEX_PATH = FAISS_DIR / "chapter_index.faiss"
METADATA_PATH = FAISS_DIR / "metadata.json"


class RAGRetriever:
    """FAISS 检索器"""
    
    def __init__(self):
        self.index = None
        self.metadata = []
        self._load_index()
    
    def _load_index(self):
        """加载 FAISS 索引和元数据"""
        import tempfile
        import shutil
        
        if not INDEX_PATH.exists():
            raise FileNotFoundError(f"FAISS 索引不存在: {INDEX_PATH}，请先运行 build_embedding_index.py")
        if not METADATA_PATH.exists():
            raise FileNotFoundError(f"元数据不存在: {METADATA_PATH}")
        
        print(f"[RAG] 正在加载 FAISS 索引: {INDEX_PATH}")
        # FAISS 不支持中文路径，先复制到临时英文路径
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_index_path = Path(tmpdir) / "index.faiss"
            shutil.copy(str(INDEX_PATH), str(tmp_index_path))
            self.index = faiss.read_index(str(tmp_index_path))
            print(f"[RAG] 已从临时路径加载索引")
        
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        
        print(f"[RAG] 已加载 {self.index.ntotal} 条向量，维度 {self.index.d}")
    
    def search(self, query_text: str, top_k: int = 3) -> List[Dict]:
        """
        搜索相似章节
        
        Args:
            query_text: 查询文本（如大纲）
            top_k: 返回最相似的 k 个结果
        
        Returns:
            相似章节列表
        """
        print(f"[RAG] 正在生成查询 embedding...")
        query_embedding = get_embedding(query_text)
        if not query_embedding:
            print("[RAG] 生成 embedding 失败")
            return []
        
        # 转换为 numpy 并归一化
        query_vec = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_vec)
        
        print(f"[RAG] 正在搜索 top-{top_k}...")
        distances, indices = self.index.search(query_vec, top_k)
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # FAISS 返回 -1 表示无结果
                continue
            
            meta = self.metadata[idx]
            
            # 读取章节内容
            chapter_path = DATA_DIR / meta['txt_file']
            content = ""
            if chapter_path.exists():
                with open(chapter_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            results.append({
                'chapter_num': meta['chapter_num'],
                'txt_file': meta['txt_file'],
                'similarity': float(dist),  # 归一化后的内积 = 余弦相似度
                'summary': meta.get('summary', ''),
                'content_preview': content[:800] + "..." if len(content) > 800 else content
            })
            print(f"[RAG] 第{meta['chapter_num']}章 相似度: {dist:.4f}")
        
        return results


def search_similar_chapters(query_text: str, top_k: int = 3) -> List[Dict]:
    """便捷函数：搜索相似章节"""
    retriever = RAGRetriever()
    return retriever.search(query_text, top_k)


def get_reference_chapter_simple(outline: str, top_k: int = 3) -> str:
    """简化版参考章节获取函数，直接返回格式化文本"""
    retriever = RAGRetriever()
    results = retriever.search(outline, top_k)
    
    if not results:
        return ""
    
    reference_text = "【参考章节】\n"
    for r in results:
        reference_text += f"\n--- 第{r['chapter_num']}章 (相似度: {r['similarity']:.4f}) ---\n"
        reference_text += r['content_preview'] + "\n"
    
    return reference_text


if __name__ == "__main__":
    # 测试
    test_outline = "耿耿和余淮在大学重逢，两人尴尬地寒暄"
    retriever = RAGRetriever()
    results = retriever.search(test_outline, top_k=3)
    
    print("\n=== 检索结果 ===")
    for r in results:
        print(f"第{r['chapter_num']}章 - 相似度: {r['similarity']:.4f}")
        print(f"摘要: {r['summary'][:100]}...")
        print("-" * 30)
