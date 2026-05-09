"""
解析 all.txt，按 "第X章" 拆分，每章存为一个独立的 chapterX.txt 文件。
输出到 data/fanfic_library/ 目录下。
"""

import re
import os

INPUT_FILE = "/mnt/d/browser_download/28192/all.txt"
OUTPUT_DIR = "/mnt/d/学习资料/大模型/hello-agents/Co-creation-projects/lgs-only-NovelGenerator/data/fanfic_library"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 匹配 "第X章 " 开头的行，X 可以是中文数字或阿拉伯数字
# 注意文件里有 \r\n 换行
chapter_pattern = re.compile(r'^第[一二三四五六七八九十百千零\d]+章\s', re.MULTILINE)

# 找到所有章节标题的位置
matches = list(chapter_pattern.finditer(text))

print(f"共找到 {len(matches)} 章")

for i, match in enumerate(matches):
    start = match.start()
    # 下一章的位置（或文件末尾）
    if i + 1 < len(matches):
        end = matches[i + 1].start()
    else:
        end = len(text)
    
    chapter_text = text[start:end].strip()
    
    # 提取章节序号（"第六十四章" → 64）
    title_line = match.group()
    num_match = re.search(r'第(.+)章', title_line)
    if num_match:
        cn_num_str = num_match.group(1)
        # 中文数字转阿拉伯数字
        cn_map = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }
        # 先试阿拉伯数字
        if cn_num_str.isdigit():
            num = int(cn_num_str)
        else:
            # 转中文数字
            if cn_num_str == '十':
                num = 10
            elif '十' in cn_num_str:
                parts = cn_num_str.split('十')
                if parts[0] == '':
                    num = 10 + cn_map.get(parts[1], 0)
                else:
                    num = cn_map.get(parts[0], 0) * 10 + cn_map.get(parts[1], 0)
            else:
                num = sum(cn_map.get(c, 0) for c in cn_num_str)
        
        output_filename = f"chapter{num}.txt"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # 去掉章节标题前后的 \r
        chapter_text_clean = chapter_text.replace('\r', '')
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chapter_text_clean)
        
        # 提取标题中的副标题（"耿耿"、"耿耿余淮" 等）
        title_rest = title_line[len(num_match.group(0)):].strip()
        print(f"  [{i+1:>2}/64] 第{num}章  {title_rest}  →  {output_filename}  ({len(chapter_text_clean)} 字)")

print(f"\n完成！共 {len(matches)} 章，输出到 {OUTPUT_DIR}")
