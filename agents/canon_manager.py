"""Structured canon and fanfic setting manager."""

import json
import os
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional


@dataclass
class CharacterProfile:
    name: str
    aliases: List[str] = field(default_factory=list)
    personality: str = ""
    background: str = ""
    abilities: List[str] = field(default_factory=list)
    speech_pattern: str = ""
    relationships: Dict[str, str] = field(default_factory=dict)
    key_events: List[str] = field(default_factory=list)
    ooc_triggers: List[str] = field(default_factory=list)


@dataclass
class CanonSetting:
    work_name: str
    main_plot_summary: str = ""
    world_rules: List[str] = field(default_factory=list)
    plot_anchors: List[str] = field(default_factory=list)
    forbidden_rules: List[str] = field(default_factory=list)
    character_relationships: str = ""
    characters: Dict[str, CharacterProfile] = field(default_factory=dict)


@dataclass
class WorkMetadata:
    work_name: str
    main_plot_summary: str = ""
    world_rules: List[str] = field(default_factory=list)
    plot_anchors: List[str] = field(default_factory=list)
    forbidden_rules: List[str] = field(default_factory=list)
    character_relationships: str = ""


@dataclass
class CharacterCore:
    character_name: str
    role_identity: str = ""
    relationship_overview: str = ""
    core_traits: List[str] = field(default_factory=list)
    core_motivation: str = ""
    value_base: List[str] = field(default_factory=list)
    speech_style: List[str] = field(default_factory=list)
    behavior_habits: List[str] = field(default_factory=list)
    background_shaping_events: List[str] = field(default_factory=list)
    character_red_lines: List[str] = field(default_factory=list)


@dataclass
class StageSnapshot:
    stage_name: str
    time_position: str = ""
    completed_events: List[str] = field(default_factory=list)
    current_psychology: List[str] = field(default_factory=list)
    current_emotional_tone: List[str] = field(default_factory=list)
    known_information: List[str] = field(default_factory=list)
    unknown_information: List[str] = field(default_factory=list)
    current_behavior_boundary: List[str] = field(default_factory=list)
    speech_shift: List[str] = field(default_factory=list)
    ooc_risks: List[str] = field(default_factory=list)


@dataclass
class RelationshipSnapshot:
    character_a: str
    character_b: str
    stage_name: str
    relation_type: str = ""
    closeness_level: str = ""
    tension_source: List[str] = field(default_factory=list)
    initiative_balance: str = ""
    misunderstanding_status: str = ""
    emotion_exposure: str = ""
    interaction_pattern: List[str] = field(default_factory=list)
    relation_boundary: List[str] = field(default_factory=list)


@dataclass
class FanficWork:
    work: WorkMetadata
    characters: List[CharacterCore] = field(default_factory=list)
    stages: List[StageSnapshot] = field(default_factory=list)
    relationships: List[RelationshipSnapshot] = field(default_factory=list)


class CanonManager:
    """Reads both legacy canon settings and structured fanfic mock data."""

    def __init__(self, workspace: str = "./outputs"):
        self.workspace = workspace
        # 统一从 data/fanfic_library 读取所有作品数据（相对路径）
        self.data_dir = "./data/fanfic_library"
        os.makedirs(self.data_dir, exist_ok=True)
        self._canon_cache: Dict[str, CanonSetting] = {}
        self._structured_cache: Dict[str, FanficWork] = {}

    def _safe_name(self, work_name: str) -> str:
        return "".join(c for c in work_name if c.isalnum() or c in (" ", "-", "_")).strip()

    def _get_data_path(self, work_name: str) -> str:
        safe_name = self._safe_name(work_name) or work_name
        return os.path.join(self.data_dir, f"{safe_name}.json")

    def create_canon(self, setting: CanonSetting) -> str:
        # 统一保存为结构化格式（包含 work 和 characters）
        file_path = self._get_data_path(setting.work_name)
        data = {
            "work": {
                "work_name": setting.work_name,
                "main_plot_summary": setting.main_plot_summary,
                "world_rules": setting.world_rules,
                "plot_anchors": setting.plot_anchors,
                "forbidden_rules": setting.forbidden_rules,
                "character_relationships": setting.character_relationships,
            },
            "characters": [
                {
                    "character_name": name,
                    "role_identity": char.background[:50] if char.background else "",
                    "relationship_overview": "",
                    "core_traits": [char.personality] if char.personality else [],
                    "core_motivation": "",
                    "value_base": [],
                    "speech_style": [char.speech_pattern] if char.speech_pattern else [],
                    "behavior_habits": char.abilities if char.abilities else [],
                    "background_shaping_events": char.key_events if char.key_events else [],
                    "character_red_lines": char.ooc_triggers if char.ooc_triggers else [],
                }
                for name, char in setting.characters.items()
            ],
            "stages": [],
            "relationships": [],
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._canon_cache[setting.work_name] = setting
        return file_path

    def create_structured_work(self, work: FanficWork) -> str:
        file_path = self._get_data_path(work.work.work_name)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(work), f, ensure_ascii=False, indent=2)
        self._structured_cache[work.work.work_name] = work
        return file_path

    def load_canon(self, work_name: str) -> Optional[CanonSetting]:
        """从统一数据目录加载作品基础信息"""
        if work_name in self._canon_cache:
            return self._canon_cache[work_name]

        file_path = self._get_data_path(work_name)
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 从结构化数据中提取 work 部分
        work_data = data.get("work", {})
        characters_data = data.get("characters", [])
        
        # 转换 characters 格式
        characters = {}
        for char in characters_data:
            name = char.get("character_name", "")
            if name:
                characters[name] = CharacterProfile(
                    name=name,
                    personality=", ".join(char.get("core_traits", [])),
                    background=char.get("role_identity", ""),
                    speech_pattern=", ".join(char.get("speech_style", [])),
                    abilities=char.get("behavior_habits", []),
                    key_events=char.get("background_shaping_events", []),
                    ooc_triggers=char.get("character_red_lines", []),
                )
        
        setting = CanonSetting(
            work_name=work_data.get("work_name", work_name),
            main_plot_summary=work_data.get("main_plot_summary", ""),
            world_rules=work_data.get("world_rules", []),
            plot_anchors=work_data.get("plot_anchors", []),
            forbidden_rules=work_data.get("forbidden_rules", []),
            character_relationships=work_data.get("character_relationships", ""),
            characters=characters,
        )
        self._canon_cache[work_name] = setting
        return setting

    def load_structured_work(self, work_name: str) -> Optional[FanficWork]:
        print(f"[CanonManager] 加载结构化同人数据: {work_name}")
        if work_name in self._structured_cache:
            print(f"[CanonManager] 命中缓存: {work_name}")
            return self._structured_cache[work_name]

        file_path = self._get_data_path(work_name)
        print(f"[CanonManager] 文件路径: {file_path}")
        if not os.path.exists(file_path):
            print(f"[CanonManager] 文件不存在: {file_path}")
            return None

        print(f"[CanonManager] 读取文件...")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        work_data = data.get("work", {})
        structured = FanficWork(
            work=WorkMetadata(**work_data),
            characters=[CharacterCore(**item) for item in data.get("characters", [])],
            stages=[StageSnapshot(**item) for item in data.get("stages", [])],
            relationships=[RelationshipSnapshot(**item) for item in data.get("relationships", [])],
        )
        print(f"[CanonManager] 加载成功: {work_name}")
        print(f"[CanonManager]   - 角色数: {len(structured.characters)}")
        print(f"[CanonManager]   - 阶段数: {len(structured.stages)}")
        print(f"[CanonManager]   - 关系数: {len(structured.relationships)}")
        self._structured_cache[work_name] = structured
        return structured

    def list_canons(self) -> List[str]:
        """列出所有作品"""
        if not os.path.exists(self.data_dir):
            return []
        return sorted(f[:-5] for f in os.listdir(self.data_dir) if f.endswith(".json"))

    def list_structured_works(self) -> List[str]:
        """列出所有作品（与 list_canons 相同，统一数据源）"""
        return self.list_canons()

    def delete_canon(self, work_name: str) -> bool:
        file_path = self._get_data_path(work_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            self._canon_cache.pop(work_name, None)
            self._structured_cache.pop(work_name, None)
            return True
        return False

    def get_character_core(self, work_name: str, character_name: str) -> Optional[CharacterCore]:
        structured = self.load_structured_work(work_name)
        if not structured:
            return None
        return next((item for item in structured.characters if item.character_name == character_name), None)

    def get_character_cores(self, work_name: str, character_names: Optional[List[str]] = None) -> List[CharacterCore]:
        structured = self.load_structured_work(work_name)
        if not structured:
            return []
        if not character_names:
            return structured.characters
        return [item for item in structured.characters if item.character_name in character_names]

    def get_stage_snapshot(self, work_name: str, stage_name: str) -> Optional[StageSnapshot]:
        structured = self.load_structured_work(work_name)
        if not structured:
            return None
        return next((item for item in structured.stages if item.stage_name == stage_name), None)

    def get_relationship_snapshots(
        self,
        work_name: str,
        stage_name: str,
        character_names: Optional[List[str]] = None,
    ) -> List[RelationshipSnapshot]:
        structured = self.load_structured_work(work_name)
        if not structured:
            return []
        relationships = [item for item in structured.relationships if item.stage_name == stage_name]
        if not character_names:
            return relationships
        selected = set(character_names)
        return [
            item for item in relationships
            if item.character_a in selected and item.character_b in selected
        ]

    def get_structured_context(
        self,
        work_name: str,
        character_names: Optional[List[str]] = None,
    ) -> Dict[str, object]:
        print(f"[CanonManager] 组装结构化上下文: work={work_name}, chars={character_names}")
        structured = self.load_structured_work(work_name)
        if not structured:
            print(f"[CanonManager] 未找到结构化数据: {work_name}")
            return {}
        
        characters = self.get_character_cores(work_name, character_names)
        
        print(f"[CanonManager] 上下文组装完成:")
        print(f"[CanonManager]   - 作品: {structured.work.work_name}")
        print(f"[CanonManager]   - 筛选角色: {[c.character_name for c in characters]}")
        
        return {
            "work": structured.work,
            "characters": characters,
        }

    def get_work_prompt(self, work_name: str) -> str:
        structured = self.load_structured_work(work_name)
        if structured:
            work = structured.work
            lines = [
                f"* 作品名: {work.work_name}",
            ]
            if work.main_plot_summary:
                lines.append(f"* 主线概述: {work.main_plot_summary}")
            if work.world_rules:
                lines.append("* 世界规则:")
                lines.extend([f"  - {item}" for item in work.world_rules])
            if work.plot_anchors:
                lines.append("* 剧情锚点:")
                lines.extend([f"  - {item}" for item in work.plot_anchors])
            if work.forbidden_rules:
                lines.append("* 禁区设定:")
                lines.extend([f"  - {item}" for item in work.forbidden_rules])
            if work.character_relationships:
                lines.append(f"* 人物关系概览: {work.character_relationships}")
            return "\n".join(lines)
        return self.get_world_prompt(work_name)

    def get_character_prompt(self, work_name: str, character_names: Optional[List[str]] = None) -> str:
        structured = self.load_structured_work(work_name)
        if structured:
            characters = self.get_character_cores(work_name, character_names)
            if not characters:
                return ""
            lines = []
            for char in characters:
                lines.append(f"• {char.character_name}")
                if char.role_identity:
                    lines.append(f"  身份定位: {char.role_identity}")
                if char.relationship_overview:
                    lines.append(f"  人物关系: {char.relationship_overview}")
                if char.core_traits:
                    lines.append(f"  核心性格: {', '.join(char.core_traits)}")
                if char.core_motivation:
                    lines.append(f"  核心动机: {char.core_motivation}")
                if char.value_base:
                    lines.append(f"  价值观底色: {', '.join(char.value_base)}")
                if char.speech_style:
                    lines.append(f"  说话风格: {', '.join(char.speech_style)}")
                if char.behavior_habits:
                    lines.append(f"  行为习惯: {', '.join(char.behavior_habits)}")
                if char.background_shaping_events:
                    lines.append(f"  底色经历: {', '.join(char.background_shaping_events)}")
                if char.character_red_lines:
                    lines.append(f"  人设底线: {', '.join(char.character_red_lines)}")
                lines.append("")
            return "\n".join(lines).strip()

        canon = self.load_canon(work_name)
        if not canon:
            return ""
        lines = []
        for name, char in canon.characters.items():
            if character_names and name not in character_names:
                continue
            lines.append(f"• {name}")
            if char.aliases:
                lines.append(f"  别名: {', '.join(char.aliases)}")
            lines.append(f"  性格: {char.personality}")
            lines.append(f"  背景: {char.background}")
            lines.append(f"  能力: {', '.join(char.abilities)}")
            lines.append(f"  说话方式: {char.speech_pattern}")
            if char.relationships:
                rel_str = "; ".join([f"{k}:{v}" for k, v in char.relationships.items()])
                lines.append(f"  人际关系: {rel_str}")
            if char.key_events:
                lines.append(f"  关键事件: {', '.join(char.key_events)}")
            lines.append("")
        return "\n".join(lines).strip()

    def get_stage_prompt(self, work_name: str, stage_name: Optional[str]) -> str:
        if not stage_name:
            return ""
        stage = self.get_stage_snapshot(work_name, stage_name)
        if not stage:
            return ""
        lines = [
            "【阶段快照】",
            f"阶段名: {stage.stage_name}",
            f"时间位置: {stage.time_position}",
        ]
        if stage.completed_events:
            lines.append("已发生事件:")
            lines.extend([f"  - {item}" for item in stage.completed_events])
        if stage.current_psychology:
            lines.append("当前心理状态:")
            lines.extend([f"  - {item}" for item in stage.current_psychology])
        if stage.current_emotional_tone:
            lines.append(f"当前情绪底色: {', '.join(stage.current_emotional_tone)}")
        if stage.known_information:
            lines.append("当前已知信息:")
            lines.extend([f"  - {item}" for item in stage.known_information])
        if stage.unknown_information:
            lines.append("当前未知信息:")
            lines.extend([f"  - {item}" for item in stage.unknown_information])
        if stage.current_behavior_boundary:
            lines.append("当前行为边界:")
            lines.extend([f"  - {item}" for item in stage.current_behavior_boundary])
        if stage.speech_shift:
            lines.append(f"说话偏移: {', '.join(stage.speech_shift)}")
        if stage.ooc_risks:
            lines.append("阶段 OOC 风险:")
            lines.extend([f"  - {item}" for item in stage.ooc_risks])
        return "\n".join(lines)

    def get_relationship_prompt(
        self,
        work_name: str,
        stage_name: Optional[str],
        character_names: Optional[List[str]] = None,
    ) -> str:
        if not stage_name:
            return ""
        relationships = self.get_relationship_snapshots(work_name, stage_name, character_names)
        if not relationships:
            return ""
        lines = ["【关系快照】"]
        for rel in relationships:
            lines.append(f"• {rel.character_a} - {rel.character_b}")
            if rel.relation_type:
                lines.append(f"  当前关系: {rel.relation_type}")
            if rel.closeness_level:
                lines.append(f"  亲密度: {rel.closeness_level}")
            if rel.tension_source:
                lines.append(f"  张力来源: {', '.join(rel.tension_source)}")
            if rel.initiative_balance:
                lines.append(f"  主动/退缩: {rel.initiative_balance}")
            if rel.misunderstanding_status:
                lines.append(f"  误会状态: {rel.misunderstanding_status}")
            if rel.emotion_exposure:
                lines.append(f"  情感表达: {rel.emotion_exposure}")
            if rel.interaction_pattern:
                lines.append(f"  互动模式: {', '.join(rel.interaction_pattern)}")
            if rel.relation_boundary:
                lines.append(f"  关系边界: {', '.join(rel.relation_boundary)}")
            lines.append("")
        return "\n".join(lines).strip()

    def get_world_prompt(self, work_name: str) -> str:
        canon = self.load_canon(work_name)
        if not canon:
            return ""
        lines = [
            f"作品: {canon.work_name}",
        ]
        if canon.main_plot_summary:
            lines.append(f"主线概述: {canon.main_plot_summary}")
        if canon.world_rules:
            lines.append("世界规则:")
            lines.extend([f"  - {rule}" for rule in canon.world_rules])
        if canon.plot_anchors:
            lines.append("剧情锚点:")
            lines.extend([f"  - {item}" for item in canon.plot_anchors])
        if canon.forbidden_rules:
            lines.append("禁区设定:")
            lines.extend([f"  - {item}" for item in canon.forbidden_rules])
        if canon.character_relationships:
            lines.append(f"人物关系概览: {canon.character_relationships}")
        return "\n".join(lines)

    def get_ooc_checklist(
        self,
        work_name: str,
        character_names: Optional[List[str]] = None,
    ) -> str:
        structured = self.load_structured_work(work_name)
        if structured:
            lines = ["【同人一致性检查清单】"]
            character_prompt = self.get_character_prompt(work_name, character_names)
            work_prompt = self.get_work_prompt(work_name)
            for block in (work_prompt, character_prompt):
                if block:
                    lines.append(block)
            lines.append("请重点检查：角色是否 OOC、是否触碰禁区设定。")
            return "\n\n".join(lines)

        canon = self.load_canon(work_name)
        if not canon:
            return ""
        lines = ["【OOC检查项】", "审核时请检查以下内容：", ""]
        for name, char in canon.characters.items():
            if character_names and name not in character_names:
                continue
            lines.append(f"• {name}")
            lines.append(f"  - 性格是否符合: {char.personality}")
            lines.append(f"  - 说话方式是否一致: {char.speech_pattern}")
            lines.append("  - 是否使用了不符合其背景的能力")
            if char.ooc_triggers:
                lines.append(f"  - 避免 OOC 场景: {', '.join(char.ooc_triggers)}")
            lines.append("")
        if canon.forbidden_rules:
            lines.append("禁区设定:")
            lines.extend([f"  - {item}" for item in canon.forbidden_rules])
        return "\n".join(lines).strip()
