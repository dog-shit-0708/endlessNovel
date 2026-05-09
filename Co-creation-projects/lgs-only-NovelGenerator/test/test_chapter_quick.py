"""快速测试章节生成Agent - 仅生成第1章的Prompt"""
from dotenv import load_dotenv
load_dotenv()

import os
import sys

# 添加项目根目录到 Python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from hello_agents import HelloAgentsLLM
from agents.chapter_generate_agent import ChapterGenerateAgent

# 配置
WORKSPACE = "./outputs"
NOVEL_ID = "test_novel_1777531274"
NOVEL_TITLE = "高中日常之课间打水"

def main():
    print("=" * 80)
    print("ChapterGenerateAgent Prompt 测试 - 仅生成第1章Prompt")
    print("=" * 80)
    
    # 1. 初始化 Agent (不需要LLM，但保留参数兼容性)
    chapter_agent = ChapterGenerateAgent(
        name="章节生成助手",
        llm=HelloAgentsLLM(),  # 不会实际调用
        workspace=WORKSPACE,
        chapter_length=2000
    )
    
    # 2. 确保存储初始化
    chapter_agent._ensure_storage(NOVEL_ID, NOVEL_TITLE)
    
    # 3. 获取第1章大纲
    print(f"\n[Main] 读取第1章大纲...")
    outline = chapter_agent.get_outline(NOVEL_ID, chapter_num=1)
    print(f"[Main] 大纲长度: {len(outline)} 字符")
    
    # 4. 生成第1章的Prompt (带RAG参考章节)
    print(f"\n[Main] 生成第1章 Prompt...")
    print(f"\n[Main] 正在检索参考章节...")
    reference_chapter = chapter_agent.get_reference_chapter(NOVEL_ID, chapter_num=1, top_k=2)
    print(f"[Main] 参考章节长度: {len(reference_chapter)} 字符")
    
    user_input = "第一章'偶遇之后'：耿耿结束拍摄后收到余淮微信约吃饭，提前到餐厅等待，回想九年来设想过的重逢场景。余淮迟到十分钟，穿着深灰色外套，头发比高中时短，坐下后说'路上堵车'，两人陷入短暂沉默。"
    
    prompt = chapter_agent.get_prompt(
        outline=outline,
        reference_chapter=reference_chapter,
        prev_summaries="无",
        user_input=user_input,
        novel_id=NOVEL_ID,
        chapter_length=2000
    )
    
    # 5. 显示完整 Prompt
    print(f"\n{'='*60}")
    print("[ChapterGenerateAgent] 完整 Prompt 内容:")
    print(f"{'='*60}")
    try:
        print(prompt)
    except UnicodeEncodeError:
        print(prompt.encode('utf-8', errors='ignore').decode('utf-8'))
    
    print(f"\n{'='*60}")
    print("[Main] 第1章 Prompt 生成完毕!")
    print(f"{'='*60}")
    print(f"Prompt 总长度: {len(prompt)} 字符")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
