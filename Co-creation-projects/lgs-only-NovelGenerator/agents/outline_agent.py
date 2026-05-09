from dotenv import load_dotenv

load_dotenv()

from typing import List, Optional

from hello_agents import HelloAgentsLLM, SimpleAgent

from agents.canon_manager import CanonManager
from agents.note_storage import SimpleNoteStorage, extract_note_id
from agents.prompt import OUTLINE_PROMPT


class OutlineAgent(SimpleAgent):
    """Outline generator with optional fanfic context."""

    def __init__(self, name: str, llm: HelloAgentsLLM = HelloAgentsLLM(), **kwargs):
        self.workspace = kwargs.pop("workspace", "./outputs")
        super().__init__(name=name, llm=llm)
        self.outline_length = 3000
        self.note_storages = {}
        self.canon_manager = CanonManager(self.workspace)
        self.current_canon: Optional[str] = kwargs.get("canon_work_name")

    def _ensure_storage(self, novel_id: str, title: str = None):
        if not self.note_storages.get(novel_id):
            if not title:
                raise ValueError(f"Storage for novel_id {novel_id} not initialized and title not provided.")
            self.note_storages[novel_id] = SimpleNoteStorage(
                f"{self.workspace}/{title}-{novel_id}/outline"
            )

    def set_canon(self, work_name: str):
        self.current_canon = work_name

    def get_canon_prompts(
        self,
        work_name: Optional[str],
        main_characters: Optional[List[str]] = None,
    ) -> tuple[str, str]:
        print(f"[OutlineAgent] 获取同人提示词: work={work_name}, chars={main_characters}")
        if not work_name:
            print("[OutlineAgent] 无作品名，返回空")
            return "", ""

        work_prompt = self.canon_manager.get_work_prompt(work_name)
        character_prompt = self.canon_manager.get_character_prompt(work_name, main_characters)
        combined = "\n\n".join(
            [part for part in (character_prompt,) if part]
        )
        
        print(f"[OutlineAgent] 提示词组装完成:")
        print(f"[OutlineAgent]   - 原作档案长度: {len(work_prompt)} 字符")
        print(f"[OutlineAgent]   - 角色信息长度: {len(combined)} 字符")
        
        return work_prompt, combined

    def run(self, user_input: str, **kwargs) -> tuple[str, str]:
        print(f"\n{'='*60}")
        print("[OutlineAgent] 开始生成大纲")
        print(f"{'='*60}")
        
        novel_id = kwargs.pop("novel_id", None)
        assert novel_id, "请提供小说ID"

        title = kwargs.pop("title", None)
        assert title, "请提供小说标题"

        is_fanfic = kwargs.pop("is_fanfic", False)
        work_name = kwargs.pop("work_name", kwargs.pop("canon_work_name", self.current_canon))
        main_characters = kwargs.pop("main_characters", None)
        
        print(f"[OutlineAgent] 参数:")
        print(f"[OutlineAgent]   - novel_id: {novel_id}")
        print(f"[OutlineAgent]   - title: {title}")
        print(f"[OutlineAgent]   - is_fanfic: {is_fanfic}")
        print(f"[OutlineAgent]   - work_name: {work_name}")
        print(f"[OutlineAgent]   - main_characters: {main_characters}")
        
        if work_name:
            self.current_canon = work_name

        self._ensure_storage(novel_id, title)
        target_length = kwargs.pop("target_length", self.outline_length)
        
        print(f"[OutlineAgent] 获取同人上下文...")
        canon_world, canon_characters = self.get_canon_prompts(
            work_name if is_fanfic else self.current_canon,
            main_characters=main_characters,
        )

        print(f"[OutlineAgent] 组装Prompt...")
        context = OUTLINE_PROMPT.format(
            user_input=user_input,
            title=title or "无",
            tags="，".join([str(tag) for tag in kwargs.values() if tag]) or "无",
            canon_world=canon_world or "无（原创模式）",
            canon_characters=canon_characters or "无（原创模式）",
            target_length=target_length,
        )
        
        print(f"[OutlineAgent] Prompt长度: {len(context)} 字符")
        print(f"\n{'='*60}")
        print("[OutlineAgent] 完整Prompt内容:")
        print(f"{'='*60}")
        print(context)
        print(f"{'='*60}\n")
        print(f"[OutlineAgent] 调用LLM生成...")

        messages = [{"role": "user", "content": context}]
        response = self.llm.invoke(messages)
        
        print(f"[OutlineAgent] LLM返回长度: {len(response)} 字符")
        print(f"[OutlineAgent] 保存大纲...")
        
        create_output = self.note_storages[novel_id].create(
            title=f"{novel_id}-大纲",
            content=response,
            note_type="outline",
            tags=["outline"],
        )
        note_id = extract_note_id(create_output)
        
        print(f"[OutlineAgent] 大纲保存成功: {note_id}")
        print(f"{'='*60}\n")
        
        return response, note_id

    def get_outline(self, novel_id: str, note_id: str, title: str = None) -> str:
        if title:
            self._ensure_storage(novel_id, title)
        return self.note_storages[novel_id].read(note_id)

    def del_outline(self, novel_id: str, note_id: str, title: str = None):
        if title:
            self._ensure_storage(novel_id, title)
        self.note_storages[novel_id].delete(note_id)

    def update_outline(self, novel_id: str, note_id: str, title: str = None, **kwargs):
        if title:
            self._ensure_storage(novel_id, title)
        self.note_storages[novel_id].update(note_id, **kwargs)
