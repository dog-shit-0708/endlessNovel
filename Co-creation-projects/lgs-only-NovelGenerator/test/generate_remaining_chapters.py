#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成婚后生活剩余章节（第2-12章）
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.bootstrap import build_container

# 配置
NOVEL_ID = "test_novel_1777111047"
TITLE = "婚后生活"
OUTLINE_ID = "note_1"

# 章节规划（根据大纲）
CHAPTERS = [
    {
        "num": 2,
        "title": "第二章-家长",
        "idea": "双方家长见面吃饭。余淮母亲无意中提到'那几年小淮吃了不少苦'，耿耿发现她对余淮那几年的了解几乎为零。"
    },
    {
        "num": 3,
        "title": "第三章-婚纱",
        "idea": "耿耿试婚纱，余淮陪她。余淮看着穿婚纱的耿耿突然红了眼眶，他说不出漂亮话，只是反复说'好看'。"
    },
    {
        "num": 4,
        "title": "第四章-请柬",
        "idea": "一起写请柬，讨论邀请哪些人。耿耿发现余淮没有邀请他大学时期最好的朋友，余淮说：'那几年我没怎么跟人联系。'"
    },
    {
        "num": 5,
        "title": "第五章-旧物",
        "idea": "耿耿收拾旧物，发现高中时的日记和照片。她在日记里看到自己写过'余淮大概永远不会知道，我有多想和他去一个城市'。"
    },
    {
        "num": 6,
        "title": "第六章-坦白",
        "idea": "耿耿主动约余淮谈话，想要一个答案。余淮终于开口，讲了那几年——母亲生病、他拼命读书、不敢联系耿耿是因为觉得自己配不上她。"
    },
    {
        "num": 7,
        "title": "第七章-冷战",
        "idea": "谈话后两人陷入短暂的沉默期。余淮每天还是会给耿耿发消息，但内容变得很克制——'今天吃了吗''早点睡'。"
    },
    {
        "num": 8,
        "title": "第八章-和解",
        "idea": "耿耿去余淮家，看到他书桌上还放着她高中时送他的照片。耿耿说：'余淮，我不是要你道歉，我是要你以后别再一个人扛了。'"
    },
    {
        "num": 9,
        "title": "第九章-婚礼彩排",
        "idea": "婚礼前一周的彩排。余淮在念誓词环节卡住了，最后只说了一句：'耿耿，我会用一辈子来证明，你选我没有错。'"
    },
    {
        "num": 10,
        "title": "第十章-前夜",
        "idea": "婚礼前一晚，两人各自在家。耿耿收到余淮发来的长消息——他第一次用文字说了那么多话。她只回了一句：'明天见。'"
    },
    {
        "num": 11,
        "title": "第十一章-婚礼",
        "idea": "婚礼当天。余淮在交换戒指时手在发抖，耿耿笑着握住他的手。两人在舞池里，余淮说：'以后想做什么，我都陪你。'"
    },
    {
        "num": 12,
        "title": "第十二章-婚后第一天",
        "idea": "婚礼后的早晨，两人在厨房一起做早餐。余淮突然说：'耿耿，谢谢你愿意嫁给我。'耿耿笑着回：'余淮，谢谢你终于学会说话了。'"
    },
]

def main():
    print("=" * 60)
    print("生成《婚后生活》第2-12章")
    print("=" * 60)
    
    # 初始化容器
    container = build_container()
    chapter_agent = container.chapter_agent
    
    for chapter in CHAPTERS:
        print(f"\n{'='*60}")
        print(f"生成第{chapter['num']}章: {chapter['title']}")
        print(f"{'='*60}")
        
        try:
            chapter_data, note_id = chapter_agent.run(
                user_input=chapter['idea'],
                novel_id=NOVEL_ID,
                novel_title=TITLE,
                chapter_num=chapter['num'],
                chapter_length=2000,
            )
            
            print(f"✅ 第{chapter['num']}章生成成功!")
            print(f"   note_id: {note_id}")
            print(f"   标题: {chapter_data.get('title', 'N/A')}")
            print(f"   摘要: {chapter_data.get('summary', 'N/A')[:100]}...")
            
        except Exception as e:
            print(f"❌ 第{chapter['num']}章生成失败: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*60}")
    print("全部章节生成完成!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
