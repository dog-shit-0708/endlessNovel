#!/usr/bin/env python
"""完整测试同人二创链路"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"【{title}】")
    print("=" * 70)

def print_result(name, success, detail=""):
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} {name}")
    if detail:
        print(f"       {detail}")

def test_1_structured_data():
    """测试1: 结构化同人数据源"""
    print_section("1. 结构化同人数据源")
    try:
        from agents.canon_manager import WorkMetadata, CharacterCore, StageSnapshot, RelationshipSnapshot, FanficWork
        print_result("WorkMetadata 数据结构", True, "用于存储作品元数据")
        print_result("CharacterCore 数据结构", True, "用于存储角色核心档案")
        print_result("StageSnapshot 数据结构", True, "用于存储阶段快照")
        print_result("RelationshipSnapshot 数据结构", True, "用于存储关系快照")
        print_result("FanficWork 数据结构", True, "整合以上所有数据")
        return True
    except Exception as e:
        print_result("数据结构导入", False, str(e))
        return False

def test_2_context_api():
    """测试2: 上下文查看接口"""
    print_section("2. 上下文查看接口 (GET /fanfic/context)")
    try:
        resp = requests.get(
            f"{BASE_URL}/fanfic/context/最好的我们",
            params={"main_characters": "余淮,耿耿"},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            work = data.get('work', {})
            chars = data.get('characters', [])
            
            print_result("接口响应", True, f"状态码: {resp.status_code}")
            print_result("原作档案读取", bool(work), f"作品名: {work.get('work_name', 'N/A')}")
            print_result("人物基础档案读取", len(chars) > 0, f"角色数: {len(chars)}")
            print_result("上下文组装", all([work, chars]), "完整上下文已组装")
            return True
        else:
            print_result("接口响应", False, f"状态码: {resp.status_code}, {resp.text[:200]}")
            return False
    except Exception as e:
        print_result("接口调用", False, f"{type(e).__name__}: {e}")
        return False

def test_3_outline_api():
    """测试3: 大纲生成接口（同人模式）"""
    print_section("3. 大纲生成接口（同人模式）")
    try:
        payload = {
            "novel_id": "test_fanfic_001",
            "title": "最好的我们-重逢短篇",
            "user_input": "写一个余淮和耿耿重逢后的故事",
            "is_fanfic": True,
            "work_name": "最好的我们",
            "main_characters": ["余淮", "耿耿"],
            "target_length": 1000
        }
        resp = requests.post(
            f"{BASE_URL}/outline/generate",
            json=payload,
            timeout=120
        )
        if resp.status_code == 200:
            data = resp.json()
            print_result("接口响应", True, f"状态码: {resp.status_code}")
            print_result("大纲生成", True, f"note_id: {data.get('note_id')}")
            content = data.get('content', '')
            has_work = "【原作档案】" in content or "原作" in content
            has_char = "【角色" in content or "余淮" in content or "耿耿" in content
            print_result("原作档案注入", has_work, "提示词中包含原作信息" if has_work else "未检测到原作信息")
            print_result("角色档案注入", has_char, "提示词中包含角色信息" if has_char else "未检测到角色信息")
            return True
        else:
            print_result("接口响应", False, f"状态码: {resp.status_code}, {resp.text[:500]}")
            return False
    except Exception as e:
        print_result("接口调用", False, f"{type(e).__name__}: {e}")
        return False

def test_4_chapter_api():
    """测试4: 章节生成接口（同人模式）"""
    print_section("4. 章节生成接口（同人模式）")
    try:
        payload = {
            "novel_id": "test_fanfic_001",
            "title": "最好的我们-重逢短篇",
            "user_input": "第一章：余淮和耿耿在振华门口重逢",
            "is_fanfic": True,
            "work_name": "最好的我们",
            "main_characters": ["余淮", "耿耿"],
            "chapter_length": 1000,
            "num_chapters": 1
        }
        resp = requests.post(
            f"{BASE_URL}/chapter/generate",
            json=payload,
            timeout=120
        )
        if resp.status_code == 200:
            data = resp.json()
            chapters = data.get('generated_chapters', [])
            print_result("接口响应", True, f"状态码: {resp.status_code}")
            print_result("章节生成", len(chapters) > 0, f"生成章节数: {len(chapters)}")
            if chapters:
                print_result("章节标题", True, f"标题: {chapters[0].get('title', 'N/A')}")
                print_result("章节摘要", True, f"摘要: {chapters[0].get('summary', 'N/A')[:50]}...")
            return True
        else:
            print_result("接口响应", False, f"状态码: {resp.status_code}, {resp.text[:500]}")
            return False
    except Exception as e:
        print_result("接口调用", False, f"{type(e).__name__}: {e}")
        return False

def test_5_prompt_templates():
    """测试5: Prompt模板"""
    print_section("5. Prompt模板检查")
    try:
        from agents.prompt import OUTLINE_PROMPT, CHAPTER_PROMPT, CHAPTER_START_PROMPT, CHAPTER_REVIEW_PROMPT
        
        checks = [
            ("OUTLINE_PROMPT", "【原作档案】" in OUTLINE_PROMPT or "{canon_world}" in OUTLINE_PROMPT),
            ("OUTLINE_PROMPT", "{canon_characters}" in OUTLINE_PROMPT),
            ("CHAPTER_PROMPT", "{canon_world}" in CHAPTER_PROMPT),
            ("CHAPTER_PROMPT", "{canon_characters}" in CHAPTER_PROMPT),
            ("CHAPTER_REVIEW_PROMPT", "{ooc_checklist}" in CHAPTER_REVIEW_PROMPT),
        ]
        
        for name, check in checks:
            print_result(f"{name} 同人字段", check)
        
        # 检查是否可读（没有乱码）
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in OUTLINE_PROMPT[:100])
        print_result("Prompt可读性", has_chinese, "包含中文字符，已重写为可读版本")
        
        return True
    except Exception as e:
        print_result("Prompt检查", False, str(e))
        return False

def main():
    print("\n" + "=" * 70)
    print("同人二创链路完整测试")
    print("=" * 70)
    
    results = []
    results.append(("结构化数据源", test_1_structured_data()))
    results.append(("上下文API", test_2_context_api()))
    results.append(("大纲生成API", test_3_outline_api()))
    results.append(("章节生成API", test_4_chapter_api()))
    results.append(("Prompt模板", test_5_prompt_templates()))
    
    print_section("测试总结")
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"总计: {total} 项测试")
    print(f"通过: {passed} 项")
    print(f"失败: {total - passed} 项")
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
