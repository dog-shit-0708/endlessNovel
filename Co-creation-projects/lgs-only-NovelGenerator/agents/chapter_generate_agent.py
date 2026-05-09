from dotenv import load_dotenv
load_dotenv()
import re
import os
import json
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from hello_agents import SimpleAgent, HelloAgentsLLM
from agents.note_storage import SimpleNoteStorage, extract_note_id
from agents.prompt import CHAPTER_PROMPT, CHAPTER_REVIEW_PROMPT, CHAPTER_START_PROMPT
from agents.rag_retriever import RAGRetriever
from agents.canon_manager import CanonManager


class MemoryItem(BaseModel):
    """记忆项数据结构"""
    node_id: str
    novel_id: str
    title: str
    content: str
    summary: str
    timestamp: datetime
    metadata: Dict[str, Any] = {}
    next_chapter_prediction: str = ""


class ChapterGenerateAgent:
    """具有上下文感知能力的 Agent"""

    def __init__(self, name: str, llm: HelloAgentsLLM = HelloAgentsLLM(), max_steps: int = 5, chapter_length: int = 3000, **kwargs):

        self.chapter_length = chapter_length
        self.max_steps = max_steps

        self.num_chapter_memories = kwargs.get("num_chapter_memories", 5)
        self.workspace = kwargs.get("workspace", "./outputs")
        self.note_storages: Dict[str, SimpleNoteStorage] = {}
        
        self.generate_agent = SimpleAgent(name="章节生成助手", llm=llm, system_prompt='你是一位擅长长篇小说结构与文本细化的专业作者助理。')
        self.review_agent = SimpleAgent(name="章节审核助手", llm=llm, system_prompt='你是一位专业的小说审核助手，负责检查章节是否符合小说的结构和风格。')

        # 内存存储
        self.memories: Dict[str, List[MemoryItem]] = {}
        
        # Canon 管理器（获取人物关系等设定）
        self.canon_manager = CanonManager()

    @staticmethod
    def extract_json_from_response(response: str) -> dict:
        """从模型输出中提取并解析 JSON"""
        # 尝试清理 Markdown 代码块标记
        clean_response = re.sub(r"```json\s*", "", response)
        clean_response = re.sub(r"```\s*$", "", clean_response)
        clean_response = clean_response.strip()
        
        try:
            return json.loads(clean_response)
        except json.JSONDecodeError as e:
            # 如果直接解析失败，尝试在文本中寻找第一个 { 和最后一个 }
            try:
                start = clean_response.find("{")
                end = clean_response.rfind("}")
                if start != -1 and end != -1:
                    json_str = clean_response[start : end + 1]
                    return json.loads(json_str)
            except Exception:
                pass
            raise ValueError(f"无法解析 JSON 响应: {response}") from e

    def _ensure_storage(self, novel_id: str, novel_title: str = None):
        if not self.note_storages.get(novel_id):
            if not novel_title:
                raise ValueError(f"Storage for novel_id {novel_id} not initialized and novel_title not provided.")
            self.note_storages[novel_id] = SimpleNoteStorage(
                workspace=os.path.join(self.workspace, f"{novel_title}-{novel_id}", 'chapters')
            )

    def get_content_from_note(self, content: str) -> str:
        try:
            # 去除 YAML 前置元数据
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if frontmatter_match:
                content = content[frontmatter_match.end():].strip()
            
            # 去除标题（第一行如果是标题）
            lines = content.split('\n')
            if lines and lines[0].startswith('# '):
                content = '\n'.join(lines[1:]).strip()
            
            return content
        except:
            return content

    def get_memories(self, novel_id: str):
        """获取最近章节记忆"""
        if not hasattr(self.note_storages[novel_id], "index"):
            self.note_storages[novel_id]._load_index()

        notes = self.note_storages[novel_id].index.get("notes", [])

        # 筛选相关章节笔记
        chapter_notes = [
            n for n in notes
            if n.get("note_type") == "chapter" and str(novel_id) in n.get("title", "")
        ]

        # 获取最后 N 章
        recent_notes = chapter_notes[-self.num_chapter_memories:]

        for note in recent_notes:
            note_id = note.get("id")
            content = self.note_storages[novel_id].read(note_id)

            if content:
                content = self.get_content_from_note(content)
                self.memories[novel_id].append(MemoryItem(
                    node_id=str(note_id),
                    title=note.get("title", "未知章节").strip(),
                    content=content,
                    novel_id=str(novel_id),
                    summary=note['tags'][0]if note.get("tags") and note['tags'] else '',
                    timestamp=datetime.fromisoformat(note.get("created_at", datetime.now().isoformat()))
                ))

    def run(self, user_input: str, **kwargs) -> str:
        """运行 Agent"""
        # 小说id用来区分小说，命名可能会重复
        novel_id = kwargs.pop("novel_id", None)
        assert novel_id, "请提供小说ID"

        novel_title = kwargs.pop("novel_title", None)
        assert novel_title, "请提供小说标题"

        self._ensure_storage(novel_id, novel_title)

        if not self.memories.get(novel_id):
            self.memories[novel_id] = []
            self.get_memories(novel_id)

        # 1. 构建上下文
        chapter_num = kwargs.get("chapter_num", 1)
        outline = self.get_outline(novel_id, chapter_num)
        reference_chapter = self.get_reference_chapter(novel_id, chapter_num)
        prev_summaries = self.get_prev_summaries(novel_id)
        chapter_length = kwargs.get("chapter_length", self.chapter_length)
        context = self.get_prompt(outline, reference_chapter, prev_summaries, user_input, novel_id, chapter_length=chapter_length)
        
        # 2. 使用上下文调用 LLM
        steps = 0
        while steps < self.max_steps:
            steps += 1

            # 生成章节内容
            response = self.generate_agent.run(context)
            try:
                response_data = self.extract_json_from_response(response)
                # 检查是否包含必要字段
                if 'title' not in response_data or 'content' not in response_data or 'next_chapter_prediction' not in response_data or 'summary' not in response_data:
                    raise ValueError("JSON 响应缺少必要字段 'title' 或 'content' 或 'next_chapter_prediction' 或 'summary'")
            except ValueError as e:
                print(f"步骤 {steps} 生成的 JSON 解析错误：{e}")
                continue
            
            # 审核章节内容
            review_context = CHAPTER_REVIEW_PROMPT.format(
                outline=outline,
                reference_chapter=reference_chapter,
                prev_summaries=prev_summaries,
                chapter_content=response_data.get('content', '')
            )
            review_response = self.review_agent.run(review_context)

            # 检查审核结果
            if "【通过】" in review_response:
                break
            
            context = self.get_prompt(outline, reference_chapter, prev_summaries, user_input, novel_id, response_data, review_response, chapter_length=chapter_length)

        # 3. 保存章节到笔记
        create_output = self.note_storages[novel_id].create(
            title=f"{response_data.get('title', '未知章节')}",
            content=response_data.get('content', ''),
            note_type="chapter",
            tags=[response_data.get('summary', '')]
        )

        # 获取章节笔记ID，保存记忆，并建立与小说ID的关联
        note_id = extract_note_id(create_output)

        self.memories[novel_id].append(MemoryItem(
            node_id=note_id,
            title=response_data.get('title', '未知章节'),
            content=response_data.get('content', ''),
            novel_id=novel_id,
            summary=response_data.get('summary', ''),
            timestamp=datetime.now().isoformat(),
            next_chapter_prediction=response_data.get('next_chapter_prediction', '')
        ))

        return response_data, note_id

    def get_prompt(self, outline: str, reference_chapter: str, prev_summaries: str, user_input: str, novel_id: str, response_data: dict = None, review_response: str = None, chapter_length: int = None, work_name: str = "最好的我们") -> str:
        """获取章节生成提示"""
        if chapter_length is None:
            chapter_length = self.chapter_length
        is_first_chapter = (prev_summaries == '无')
        
        # 获取人物关系设定
        try:
            canon = self.canon_manager.get_setting(work_name)
            character_relationships = canon.character_relationships if canon else "耿耿和余淮是高中同学，关系微妙，互有好感但未表白。"
        except Exception:
            character_relationships = "耿耿和余淮是高中同学，关系微妙，互有好感但未表白。"

        if is_first_chapter:
            prompt_template = CHAPTER_START_PROMPT
            context = prompt_template.format(
                outline=outline,
                character_relationships=character_relationships,
                reference_chapter=reference_chapter,
                chapter_history='无' if response_data is None else response_data.get('content', '无'),
                evaluation=review_response or "无",
                user_input=user_input,
                chapter_length=chapter_length
            )
        else:
            prompt_template = CHAPTER_PROMPT
            context = prompt_template.format(
                outline=outline,
                character_relationships=character_relationships,
                reference_chapter=reference_chapter,
                prev_summaries=prev_summaries,
                chapter_history='无' if response_data is None else response_data.get('content', '无'),
                evaluation=review_response or "无",
                user_input=user_input or [self.memories[novel_id][-1].next_chapter_prediction if self.memories[novel_id] else "无"][0],
                chapter_length=chapter_length
            )
        
        # 打印完整 prompt
        print(f"\n{'='*60}")
        print("[ChapterGenerateAgent] 完整 Prompt 内容:")
        print(f"{'='*60}")
        print(context)
        print(f"{'='*60}\n")
        
        return context

    def get_outline(self, novel_id: str, chapter_num: int = 1) -> str:
        """获取指定章节的大纲概要"""
        dir_path = os.path.join(os.path.dirname(self.note_storages[novel_id].workspace), "outline")
        print(f"[get_outline] 查找大纲目录: {dir_path}")
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"大纲目录不存在: {dir_path}")
        paths = [f for f in os.listdir(dir_path) if f.endswith('.md') and f != 'index.md']
        print(f"[get_outline] 找到md文件: {paths}")
        assert len(paths) >= 1, f"目录 {dir_path} 下应该有大纲文件"
        # 取第一个md文件
        path = os.path.join(dir_path, paths[0])
        print(f"[get_outline] 读取文件: {path}")
        with open(path, "r", encoding='utf-8') as f:
            full_outline = f.read()
        
        # 提取指定章节的大纲内容
        return self._extract_chapter_outline(full_outline, chapter_num)
    
    def _extract_chapter_outline(self, full_outline: str, chapter_num: int) -> str:
        """从完整大纲中提取指定章节的内容"""
        lines = full_outline.split('\n')
        
        # 支持中文数字：1->一, 2->二
        chinese_nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        if chapter_num <= 10:
            chapter_cn = chinese_nums[chapter_num]
        else:
            chapter_cn = str(chapter_num)
        
        # 查找 "### 第X章" 或 "### 第X章" 的起始位置
        patterns = [f"### 第{chapter_num}章", f"### 第{chapter_cn}章"]
        start_idx = -1
        for i, line in enumerate(lines):
            for pattern in patterns:
                if line.strip().startswith(pattern):
                    start_idx = i
                    print(f"[_extract_chapter_outline] 找到章节标记: {line.strip()[:20]}...")
                    break
            if start_idx != -1:
                break
        
        if start_idx == -1:
            print(f"[_extract_chapter_outline] 未找到第{chapter_num}章（尝试匹配: {patterns}），返回全量大纲")
            return self.get_content_from_note(full_outline)
        
        # 查找下一章的起始位置（匹配阿拉伯数字或中文数字）
        end_idx = len(lines)
        for i in range(start_idx + 1, len(lines)):
            if re.match(r'^### 第[\d一二三四五六七八九十]+章', lines[i].strip()):
                end_idx = i
                break
        
        # 提取当前章节的内容
        chapter_lines = lines[start_idx:end_idx]
        chapter_content = '\n'.join(chapter_lines)
        
        print(f"[_extract_chapter_outline] 提取第{chapter_num}章，长度: {len(chapter_content)} 字符")
        return chapter_content.strip()

    def get_reference_chapter(self, novel_id: str, chapter_num: int, top_k: int = 3) -> str:
        """通过 RAG 检索获取参考章节内容

        用当前章节的大纲做 embedding，从 FAISS 检索最相关的章节，
        然后读取 txt/ 目录下的对应全文。
        """
        # 1. 拿当前大纲
        outline = self.get_outline(novel_id, chapter_num)
        print(f"[get_reference_chapter] 大纲长度: {len(outline)} 字符")

        # 2. 使用 FAISS 检索
        print(f"[get_reference_chapter] 正在使用 FAISS 检索 top-{top_k}...")
        try:
            retriever = RAGRetriever()
            results = retriever.search(outline, top_k=top_k)
            print(f"[get_reference_chapter] 检索完成，找到 {len(results)} 个结果")
        except Exception as e:
            print(f"[get_reference_chapter] FAISS 检索失败: {e}")
            import traceback
            traceback.print_exc()
            return "无"

        if not results:
            print(f"[get_reference_chapter] 未找到相关章节")
            return "无"

        # 3. 组装参考内容
        reference_parts = []
        for r in results:
            chapter_num_str = str(r['chapter_num'])
            similarity = r['similarity']
            # 读取完整内容（RAGRetriever 已读取预览，这里直接取预览即可）
            content = r.get('content_preview', '')
            reference_parts.append(
                f"【参考章节-第{chapter_num_str}章（相似度: {similarity:.2f}）】\n{content[:2000]}"
            )
            print(f"[get_reference_chapter] 已读取第{chapter_num_str}章，相似度: {similarity:.4f}")

        print(f"[get_reference_chapter] 共找到 {len(reference_parts)} 个参考章节")
        if not reference_parts:
            return "无"

        return "\n\n".join(reference_parts)

    def get_prev_summaries(self, novel_id: str):
        if self.memories.get(novel_id):
            return "\n".join([f"【{mem.title}】\n{mem.summary}" for mem in self.memories[novel_id][-self.num_chapter_memories:]])
        return "无"
    
    def del_chapter(self, novel_id:str, note_id: str, novel_title: str = None):
        """删除章节"""
        if novel_title:
            self._ensure_storage(novel_id, novel_title)
        self.note_storages[novel_id].delete(note_id)
        # 从记忆中删除该章节
        if self.memories.get(novel_id):
            self.memories[novel_id] = [mem for mem in self.memories[novel_id] if mem.node_id != note_id]

    def update_chapter(self, novel_id:str, note_id: str, novel_title: str = None, **kwargs):
        """更新章节"""
        if novel_title:
            self._ensure_storage(novel_id, novel_title)
        self.note_storages[novel_id].update(note_id, **kwargs)
        # 更新记忆中的章节内容
        if self.memories.get(novel_id):
            for mem in self.memories[novel_id]:
                if mem.node_id == note_id:
                    mem.title = kwargs.get('title', mem.title)
                    mem.content = kwargs.get('content', mem.content)
                    mem.summary = kwargs.get('summary', mem.summary)
                    mem.next_chapter_prediction = kwargs.get('next_chapter_prediction', mem.next_chapter_prediction)
                    mem.timestamp = datetime.now().isoformat()
                    break

def main():
    print("=" * 80)
    print("Novel ChapterGenerateAgent 示例")
    print("=" * 80 + "\n")

    # llm = HelloAgentsLLM(model="qwen3:0.6b", api_key="ollama", base_url="http://127.0.0.1:11434/v1", provider='ollama')
    llm = HelloAgentsLLM(provider='qwen')
    novel_id = "demo_novel_001"
    novel_title = "记忆之城"

    # 1. 模拟大纲文件存在
    # 因为 ChapterGenerateAgent.get_outline 依赖于文件系统查找大纲
    # 我们手动创建一个假的大纲文件用于测试
    workspace_root = "./outputs"
    # 注意：这里模拟 OutlineAgent 的输出路径结构
    outline_dir = os.path.join(workspace_root, f"{novel_title}-{novel_id}", "outline")
    if not os.path.exists(outline_dir):
        os.makedirs(outline_dir)
    
    # 清理旧文件以确保测试环境干净
    for f in os.listdir(outline_dir):
        try:
            os.remove(os.path.join(outline_dir, f))
        except Exception:
            pass
        
    dummy_outline_content = """---
tags: [outline]
created_at: 2025-01-27T10:00:00
---
# 记忆之城-大纲

## 核心梗概
一位能与城市记忆对话的年轻人，在拆迁浪潮中发现一段被刻意抹去的历史。

## 主要人物
- 李寻：主角，拥有"读取"物体记忆的能力。
- 陈叔：古董店老板，似乎知道李寻身世的秘密。

## 故事走向
1. 觉醒能力，卷入拆迁冲突。
2. 发现神秘物品，引出旧事。
3. ...
"""
    dummy_outline_path = os.path.join(outline_dir, f"{novel_id}-outline.md")
    with open(dummy_outline_path, "w", encoding="utf-8") as f:
        f.write(dummy_outline_content)

    print(f"已创建模拟大纲文件: {dummy_outline_path}")
    
    # 2. 初始化章节生成 Agent
    chapter_agent = ChapterGenerateAgent(
        name="小说章节助手",
        llm=llm,
        workspace=workspace_root,  # 使用与 OutlineAgent 一致的根目录
        chapter_length=1000 # 演示用，设短一点
    )

    # 3. 生成第一章
    print(f"\n正在生成第一章...")
    try:
        # run 方法需要 novel_title 来定位目录
        chapter_data_1, note_id_1 = chapter_agent.run(
            user_input="第一章需要通过一个具体的拆迁冲突场景，引出主角的能力。主角李寻在试图保护一家老店不被强拆时，无意中听到了推土机的'心声'。",
            novel_id=novel_id,
            novel_title=novel_title 
        )
        print(f"第一章生成完成，Note ID: {note_id_1}")
        print(f"标题: {chapter_data_1.get('title')}")
        print(f"摘要: {chapter_data_1.get('summary')}")
        print(f"下一章预测: {chapter_data_1.get('next_chapter_prediction')}")

        # 4. 生成第二章（会自动读取第一章作为上下文）
        print(f"\n正在生成第二章...")
        chapter_data_2, note_id_2 = chapter_agent.run(
            user_input="主角在废墟中发现了一个奇怪的物品，触发了回忆。那个物品似乎在呼唤他。",
            novel_id=novel_id,
            novel_title=novel_title
        )
        print(f"第二章生成完成，Note ID: {note_id_2}")
        print(f"标题: {chapter_data_2.get('title')}")
        print(f"摘要: {chapter_data_2.get('summary')}")
        
    except Exception as e:
        print(f"生成过程中出错: {e}")
        import traceback
        traceback.print_exc()



if __name__ == "__main__":
    main()
