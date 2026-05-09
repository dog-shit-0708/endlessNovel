"""快速测试大纲生成 Agent"""
import sys
import os
sys.path.append(os.getcwd())

from agents.outline_agent import OutlineAgent
from hello_agents import HelloAgentsLLM

def test_outline():
    # 初始化
    llm = HelloAgentsLLM()
    agent = OutlineAgent(name="TestOutline", llm=llm)
    
    # 测试同人模式
    result, note_id = agent.run(
        user_input="写一个耿耿和余淮重逢后第一次单独吃饭的场景，要有暧昧氛围但不要太直白",
        novel_id="test_001",
        title="测试同人",
        is_fanfic=True,
        work_name="最好的我们",
        main_characters=["耿耿", "余淮"],
        target_length=1000,
    )
    
    print(f"\n生成完成！Note ID: {note_id}")
    print(f"大纲长度: {len(result)} 字符")
    return result

if __name__ == "__main__":
    test_outline()
