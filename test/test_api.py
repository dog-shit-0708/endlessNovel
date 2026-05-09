"""
API 测试脚本 - 古风悬疑主题
直接调用 FastAPI 接口测试
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

# 测试配置
novel_id = f"novel_{int(time.time())}"
title = "长安诡事录"
print(f"测试配置:\n小说ID: {novel_id}\n标题: {title}\n")

# ==================== 1. 生成大纲 ====================
print("\n" + "="*60)
print("步骤1: 生成大纲")
print("="*60)

outline_data = {
    "novel_id": novel_id,
    "title": title,
    "user_input": "唐朝长安城，一位落第书生因偶然得到一枚神秘玉佩，能看见死者临终前看到的画面，于是与一位女仵作联手侦破连环命案的故事。",
    "tags": ["古风", "悬疑", "推理", "唐朝"],
    "target_length": 1000,
    "style_tags": {
        "channel": "男频",
        "style": "悬疑"
    }
}

print(f"请求数据: {json.dumps(outline_data, ensure_ascii=False, indent=2)}")
start_time = time.time()

response = requests.post(f"{BASE_URL}/outline/generate", json=outline_data)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    outline_note_id = result["note_id"]
    print(f"大纲生成成功!")
    print(f"Note ID: {outline_note_id}")
    print(f"耗时: {time.time() - start_time:.2f} 秒")
    print(f"大纲预览 (前300字):\n{result['content'][:300]}...")
else:
    print(f"错误: {response.text}")
    exit(1)

# ==================== 2. 获取大纲 ====================
print("\n" + "="*60)
print("步骤2: 获取大纲验证")
print("="*60)

response = requests.get(f"{BASE_URL}/outline/{title}/{novel_id}/{outline_note_id}")
if response.status_code == 200:
    print("获取大纲成功!")
    print(f"内容长度: {len(response.json()['content'])} 字")
else:
    print(f"错误: {response.text}")

# ==================== 3. 生成章节 ====================
print("\n" + "="*60)
print("步骤3: 生成第一章")
print("="*60)

chapter_data = {
    "novel_id": novel_id,
    "title": title,
    "user_input": "第一章：长安城发生离奇命案，死者死状诡异。主角书生在停尸房意外触碰尸体，玉佩发光，他看到了死者临死前的恐怖画面。",
    "num_chapters": 1,
    "chapter_length": 1000
}

print(f"请求数据: {json.dumps(chapter_data, ensure_ascii=False, indent=2)}")
start_time = time.time()

response = requests.post(f"{BASE_URL}/chapter/generate", json=chapter_data)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"章节生成成功!")
    print(f"耗时: {time.time() - start_time:.2f} 秒")
    
    for chapter in result["generated_chapters"]:
        chapter_note_id = chapter["id"]
        print(f"\n章节ID: {chapter_note_id}")
        print(f"标题: {chapter['title']}")
        print(f"摘要: {chapter['summary']}")
else:
    print(f"错误: {response.text}")
    exit(1)

# ==================== 4. 获取章节内容 ====================
print("\n" + "="*60)
print("步骤4: 获取章节完整内容")
print("="*60)

response = requests.get(f"{BASE_URL}/chapter/{title}/{novel_id}/{chapter_note_id}")
if response.status_code == 200:
    content = response.json()["content"]
    print(f"内容长度: {len(content)} 字")
    print(f"\n内容预览 (前500字):\n{'-'*40}")
    print(content[:500] + "...")
    print('-'*40)
else:
    print(f"错误: {response.text}")

# ==================== 5. 获取项目信息 ====================
print("\n" + "="*60)
print("步骤5: 获取项目信息")
print("="*60)

response = requests.get(f"{BASE_URL}/projects/{title}/{novel_id}")
if response.status_code == 200:
    project = response.json()
    print(f"项目信息:")
    print(f"  小说ID: {project['novel_id']}")
    print(f"  标题: {project['title']}")
    print(f"  大纲ID: {project['outline_id']}")
    print(f"  章节数: {len(project['chapters'])}")
    for ch in project['chapters']:
        print(f"    - {ch['title']}: {ch['summary'][:50]}...")
else:
    print(f"错误: {response.text}")

print("\n" + "="*60)
print("API 测试完成!")
print("="*60)
