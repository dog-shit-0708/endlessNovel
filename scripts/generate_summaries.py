"""
为 data/fanfic_library/ 下的 chapter1.txt ~ chapter64.txt 每章生成摘要（200字左右）。
输出为 summary1.txt ~ summary64.txt，保存在同一目录下。

使用 DeepSeek API 进行单章摘要，参数通过环境变量或 hardcode 配置。
"""

import os
import re
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "fanfic_library")
CHAPTERS_DIR = os.path.join(DATA_DIR, "txt")
SUMMARIES_DIR = DATA_DIR  # 摘要存到 fanfic_library 目录下

# 配置：从第几章开始生成摘要
START_CHAPTER = 58

# DeepSeek API 配置
API_KEY = os.getenv("LLM_API_KEY", os.getenv("DEEPSEEK_API_KEY", ""))
API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"
# 注意：deepseek 的速率限制
REQUEST_INTERVAL = 0.5  # 每次请求间隔秒数

SUMMARY_PROMPT_TEMPLATE = """为以下小说章节生成一个摘要，约200字左右。

要求：
- 概括本章核心事件和情节推进
- 体现主要人物的行为或心理变化
- 如果章节末尾有悬念或伏笔，简要提及
- 语言简洁，保持中性叙述，不要评价好坏

【章节标题】
{chapter_title}

【章节正文】
{chapter_content}

请直接输出摘要内容，不要添加额外说明。"""


def get_chapter_title(content: str) -> str:
    """从章节内容中提取标题行"""
    first_line = content.strip().split('\n')[0]
    return first_line


def summarize_chapter(title: str, content: str, chapter_num: int) -> str:
    """调用 LLM 为单章生成摘要"""
    # 截取正文（去掉标题行）
    body_lines = content.strip().split('\n')[1:]
    body = '\n'.join(body_lines).strip()
    
    # 如果正文过长，截取前8000字防止超 token
    if len(body) > 8000:
        body = body[:8000] + "\n\n[正文过长已截断]"
    
    prompt = SUMMARY_PROMPT_TEMPLATE.format(
        chapter_title=title,
        chapter_content=body
    )
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        summary = data["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        print(f"  [ERROR] 第{chapter_num}章摘要失败: {e}")
        return f"[摘要生成失败: {e}]"


def main():
    if not API_KEY:
        print("错误: 未设置 DEEPSEEK_API_KEY 环境变量")
        print("请在 .env 文件中设置或直接 export DEEPSEEK_API_KEY=your_key")
        return
    
    # 查找所有 chapterX.txt 文件
    chapter_files = []
    for f in os.listdir(CHAPTERS_DIR):
        match = re.match(r'^chapter(\d+)\.txt$', f)
        if match:
            chapter_files.append((int(match.group(1)), f))
    
    chapter_files.sort(key=lambda x: x[0])
    
    # 过滤：只处理从 START_CHAPTER 开始的章节
    chapter_files = [(num, f) for num, f in chapter_files if num >= START_CHAPTER]
    
    print(f"共找到 {len(chapter_files)} 章（从第{START_CHAPTER}章开始），开始生成摘要...\n")
    
    for num, filename in chapter_files:
        summary_filename = f"summary{num}.txt"
        summary_path = os.path.join(SUMMARIES_DIR, summary_filename)
        
        # 如果摘要已存在则跳过
        if os.path.exists(summary_path):
            print(f"  [{num}/{len(chapter_files)}] 第{num}章摘要已存在，跳过")
            continue
        
        filepath = os.path.join(CHAPTERS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        title = get_chapter_title(content)
        print(f"  [{num}/{len(chapter_files)}] 第{num}章: {title}")
        
        summary = summarize_chapter(title, content, num)
        
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        
        print(f"    → 摘要长度: {len(summary)} 字")
        print(f"    → 保存至: {summary_filename}")
        
        # 避免速率限制
        time.sleep(REQUEST_INTERVAL)
    
    print(f"\n完成！所有摘要已保存至 {SUMMARIES_DIR}")
    
    # 汇总所有摘要到一个文件
    merge_summaries()


def merge_summaries():
    """将所有 summaryX.txt 汇总成一个文件"""
    # 查找所有 summaryX.txt 文件
    summary_files = []
    for f in os.listdir(SUMMARIES_DIR):
        match = re.match(r'^summary(\d+)\.txt$', f)
        if match:
            summary_files.append((int(match.group(1)), f))
    
    summary_files.sort(key=lambda x: x[0])
    
    if not summary_files:
        print("没有找到任何摘要文件")
        return
    
    # 读取并汇总
    merged_content = []
    merged_content.append("# 小说章节摘要汇总\n")
    merged_content.append(f"共 {len(summary_files)} 章\n")
    merged_content.append("=" * 50 + "\n\n")
    
    for num, filename in summary_files:
        filepath = os.path.join(SUMMARIES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        merged_content.append(f"## 第{num}章\n")
        merged_content.append(content)
        merged_content.append("\n\n" + "-" * 50 + "\n\n")
    
    # 保存汇总文件
    merged_path = os.path.join(DATA_DIR, "all_summaries.md")
    with open(merged_path, "w", encoding="utf-8") as f:
        f.write("".join(merged_content))
    
    print(f"\n汇总文件已保存至: {merged_path}")
    print(f"共汇总 {len(summary_files)} 章摘要")


if __name__ == "__main__":
    main()
