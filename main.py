import os
import time
import sys
# Add the current directory to sys.path to ensure imports work correctly
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "agents")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from agents.outline_agent import OutlineAgent
from agents.chapter_generate_agent import ChapterGenerateAgent
from agents.canon_manager import CanonManager, CanonSetting, CharacterProfile
from hello_agents import HelloAgentsLLM

def print_step(step_name):
    print("\n" + "="*60)
    print(f"正在执行步骤: {step_name}")
    print("="*60 + "\n")

def setup_fanfiction_canon():
    """
    设置同人原作设定
    返回: (原作名称, 是否使用同人模式, 阶段名称, 主要角色列表)
    """
    print_step("0. 选择创作模式")
    print("请选择创作模式:")
    print("1. 原创小说")
    print("2. 同人二创")
    
    mode = input("请输入选项 (1/2): ").strip()
    
    if mode == "1":
        return None, False, []
    
    # 同人模式 - 检查结构化同人数据源
    canon_manager = CanonManager()
    structured_works = canon_manager.list_structured_works()
    
    if structured_works:
        print("\n已存在的结构化同人数据源:")
        for i, work in enumerate(structured_works, 1):
            print(f"  {i}. {work}")
        print("  0. 使用传统方式创建原作设定")
        
        choice = input(f"\n请选择 (0-{len(structured_works)}): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(structured_works):
            work_name = structured_works[int(choice) - 1]
            
            # 加载作品信息，显示可选角色
            work_data = canon_manager.load_structured_work(work_name)
            if work_data:
                print(f"\n【{work_name}】可用角色:")
                for i, char in enumerate(work_data.characters, 1):
                    print(f"  {i}. {char.character_name}")
                
                char_input = input(f"\n请选择主要角色 (多个用逗号分隔，如 1,2 或 直接回车选择全部): ").strip()
                if char_input:
                    char_indices = [int(x.strip()) - 1 for x in char_input.split(",") if x.strip().isdigit()]
                    main_characters = [work_data.characters[i].character_name for i in char_indices if 0 <= i < len(work_data.characters)]
                else:
                    main_characters = [c.character_name for c in work_data.characters]
                
                print(f"\n✓ 已选择: 作品={work_name}, 角色={main_characters}")
                return work_name, True, main_characters
    
    # 传统方式创建原作设定
    print("\n暂无结构化同人数据源，使用传统方式创建。")
    print("\n" + "="*60)
    print("创建原作设定")
    print("="*60)
    
    work_name = input("原作名称: ").strip()
    work_type = input("作品类型 (小说/动漫/游戏等): ").strip() or "小说"
    world_view = input("世界观概述: ").strip()
    
    world_rules = []
    print("\n世界规则 (输入空行结束):")
    while True:
        rule = input("  - ").strip()
        if not rule:
            break
        world_rules.append(rule)
    
    timeline = input("\n原作时间线/关键节点: ").strip()
    
    key_locations = []
    print("\n关键地点 (输入空行结束):")
    while True:
        loc = input("  - ").strip()
        if not loc:
            break
        key_locations.append(loc)
    
    # 创建角色
    characters = {}
    print("\n" + "="*60)
    print("添加角色 (至少添加一个主要角色)")
    print("="*60)
    
    while True:
        char_name = input("\n角色名 (输入空行结束): ").strip()
        if not char_name:
            if not characters:
                print("请至少添加一个角色!")
                continue
            break
        
        personality = input("  性格特征: ").strip()
        background = input("  背景经历: ").strip()
        speech = input("  说话方式/口头禅: ").strip()
        
        abilities = []
        print("  能力/技能 (输入空行结束):")
        while True:
            ab = input("    - ").strip()
            if not ab:
                break
            abilities.append(ab)
        
        key_events = []
        print("  关键事件/不可违背设定 (输入空行结束):")
        while True:
            ev = input("    - ").strip()
            if not ev:
                break
            key_events.append(ev)
        
        char = CharacterProfile(
            name=char_name,
            aliases=[],
            personality=personality,
            background=background,
            abilities=abilities,
            speech_pattern=speech,
            relationships={},
            key_events=key_events,
            ooc_triggers=[]
        )
        characters[char_name] = char
        print(f"  ✓ 角色 '{char_name}' 已添加")
    
    forbidden_zones = []
    print("\n二创禁区/绝对不能触碰的设定 (输入空行结束):")
    while True:
        zone = input("  - ").strip()
        if not zone:
            break
        forbidden_zones.append(zone)
    
    canon_notes = input("\n其他备注: ").strip()
    
    # 创建CanonSetting
    canon = CanonSetting(
        work_name=work_name,
        work_type=work_type,
        world_view=world_view,
        world_rules=world_rules,
        timeline=timeline,
        key_locations=key_locations,
        characters=characters,
        forbidden_zones=forbidden_zones,
        canon_notes=canon_notes
    )
    
    canon_manager.create_canon(canon)
    print(f"\n✓ 原作设定 '{work_name}' 已保存")
    
    return work_name, True, []

def main():
    # 0. 选择创作模式
    canon_work, is_fanfiction, main_characters = setup_fanfiction_canon()
    
    # Configuration
    novel_id = f"test_novel_{int(time.time())}"
    
    if is_fanfiction:
        print(f"\n当前模式: 同人二创 ({canon_work})")
        title = input("同人小说标题: ").strip()
        print("\n请输入你的二创创意 (例如: '如果XX在XX时刻做了XX选择...')")
        user_idea = input("创意: ").strip()
    else:
        print("\n当前模式: 原创小说")
        title = input("小说标题: ").strip() or "长安诡事录"
        user_idea = input("创意: ").strip() or "唐朝长安城，一位落第书生因偶然得到一枚神秘玉佩，能看见死者临终前看到的画面，于是与一位女仵作联手侦破连环命案的故事。"
    
    print(f"测试配置:\n小说ID: {novel_id}\n标题: {title}\n创意: {user_idea}\n")

    # Initialize LLM
    # Assuming environment variables are set correctly for the default provider
    try:
        llm = HelloAgentsLLM()
        print("LLM 初始化成功。")
    except Exception as e:
        print(f"LLM 初始化失败: {e}")
        return

    # ---------------------------------------------------------
    # Test Outline Agent
    # ---------------------------------------------------------
    print_step("1. 初始化 OutlineAgent (大纲生成Agent)")
    try:
        outline_agent = OutlineAgent(name="TestOutlineAgent", llm=llm)
        if canon_work:
            outline_agent.set_canon(canon_work)
            print(f"OutlineAgent 初始化完成，已加载原作设定: {canon_work}")
        else:
            print("OutlineAgent 初始化完成。")
    except Exception as e:
        print(f"OutlineAgent 初始化失败: {e}")
        return

    print_step("2. 生成大纲 (Generate Outline)")
    print(f"调用 outline_agent.run，输入创意: {user_idea}")
    start_time = time.time()
    
    try:
        # 构建大纲生成参数
        outline_kwargs = {
            "user_input": user_idea,
            "novel_id": novel_id,
            "title": title,
            "tags": ["同人", "二创"] if is_fanfiction else ["原创"],
            "target_length": 1000,  # Keep it short for testing
        }
        
        # 同人模式：使用新的结构化参数
        if is_fanfiction and canon_work:
            outline_kwargs.update({
                "is_fanfic": True,
                "work_name": canon_work,
                "main_characters": main_characters,
            })
        else:
            outline_kwargs["canon_work_name"] = canon_work
        
        outline_content, outline_note_id = outline_agent.run(**outline_kwargs)
    except Exception as e:
        print(f"大纲生成失败: {e}")
        import traceback
        traceback.print_exc()
        return

    end_time = time.time()
    print(f"大纲生成耗时: {end_time - start_time:.2f} 秒。")
    print(f"生成的大纲 Note ID: {outline_note_id}")
    print("大纲内容预览 (前500字符):")
    print("-" * 30)
    print(outline_content[:500] + "...")
    print("-" * 30)

    # ---------------------------------------------------------
    # Test Chapter Generate Agent
    # ---------------------------------------------------------
    print_step("3. 初始化 ChapterGenerateAgent (章节生成Agent)")
    try:
        chapter_agent = ChapterGenerateAgent(
            name="TestChapterAgent", 
            llm=llm,
            max_steps=3, # Limit steps for testing
            chapter_length=2000, # Keep it short
            canon_work_name=canon_work
        )
        if canon_work:
            print(f"ChapterGenerateAgent 初始化完成，已加载原作设定: {canon_work}")
        else:
            print("ChapterGenerateAgent 初始化完成。")
    except Exception as e:
        print(f"ChapterGenerateAgent 初始化失败: {e}")
        return

    print_step("4. 解析大纲获取章节列表")
    
    # 从大纲内容中解析章节数量
    import re
    chapter_matches = re.findall(r'### 第[一二三四五六七八九十\d]+章[：:]', outline_content)
    total_chapters = len(chapter_matches)
    print(f"检测到大纲共 {total_chapters} 章")
    
    # 提取每章的剧情要点作为生成指引
    chapter_guidance = []
    for i, match in enumerate(chapter_matches, 1):
        # 找到该章节标题的位置
        start_idx = outline_content.find(match)
        if start_idx == -1:
            continue
        # 提取该章节的内容（到下一个###或结束）
        section_end = outline_content.find("### 第", start_idx + len(match))
        if section_end == -1:
            section_text = outline_content[start_idx:]
        else:
            section_text = outline_content[start_idx:section_end]
        
        # 提取剧情要点
        plot_match = re.search(r'\*\*剧情要点\*\*[:：]\s*(.+?)(?:\n|$)', section_text)
        if plot_match:
            guidance = plot_match.group(1).strip()[:200]  # 截取前200字
        else:
            guidance = f"第{i}章内容"
        chapter_guidance.append(guidance)
    
    print(f"已提取 {len(chapter_guidance)} 章的剧情指引")
    
    print_step("5. 循环生成所有章节")
    
    for chapter_num in range(1, total_chapters + 1):
        print(f"\n{'='*60}")
        print(f"正在生成第 {chapter_num}/{total_chapters} 章")
        print(f"{'='*60}")
        
        chapter_idea = chapter_guidance[chapter_num - 1] if chapter_num <= len(chapter_guidance) else f"第{chapter_num}章内容"
        print(f"本章指引: {chapter_idea[:100]}...")
        
        start_time = time.time()
        
        try:
            chapter_kwargs = {
                "user_input": chapter_idea,
                "novel_id": novel_id,
                "novel_title": title,
                "chapter_num": chapter_num,
            }
            
            if is_fanfiction and canon_work:
                chapter_kwargs.update({
                    "is_fanfic": True,
                    "work_name": canon_work,
                    "main_characters": main_characters,
                })
            else:
                chapter_kwargs["canon_work_name"] = canon_work
            
            chapter_data, chapter_note_id = chapter_agent.run(**chapter_kwargs)
            
            end_time = time.time()
            print(f"第{chapter_num}章生成完成！耗时: {end_time - start_time:.2f} 秒")
            print(f"标题: {chapter_data.get('title')}")
            print(f"摘要: {chapter_data.get('summary')[:100]}...")
            
        except Exception as e:
            print(f"第{chapter_num}章生成失败: {e}")
            import traceback
            traceback.print_exc()
            continue  # 继续生成下一章
    
    print(f"\n{'='*60}")
    print(f"全部 {total_chapters} 章生成完成！")
    print(f"{'='*60}")

    # ---------------------------------------------------------
    # Verification
    # ---------------------------------------------------------
    print_step("6. 验证输出文件 (Verify Output Files)")
    outline_path = os.path.join("outputs", f"{title}-{novel_id}", "outline")
    chapter_path = os.path.join("outputs", f"{title}-{novel_id}", "chapters")
    
    print(f"检查大纲目录: {outline_path}")
    if os.path.exists(outline_path) and os.listdir(outline_path):
        print("PASS: 大纲目录存在且不为空。")
    else:
        print("FAIL: 大纲目录缺失或为空。")

    print(f"检查章节目录: {chapter_path}")
    if os.path.exists(chapter_path):
        chapter_files = [f for f in os.listdir(chapter_path) if f.endswith('.md')]
        print(f"PASS: 章节目录存在，共 {len(chapter_files)} 个章节文件。")
    else:
        print("FAIL: 章节目录缺失或为空。")

    print("\n" + "="*60)
    print("测试流程结束 - 小说生成完成！")
    print("="*60)

if __name__ == "__main__":
    main()
