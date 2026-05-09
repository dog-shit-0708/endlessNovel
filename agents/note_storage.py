import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import yaml


def extract_note_id(output: str) -> str:
    match = re.search(r"ID:\s*(note_[0-9_]+)", output)
    if not match:
        raise ValueError(f"无法从输出解析 note_id:\n{output}")
    return match.group(1)


class SimpleNoteStorage:
    """Shared markdown note storage used by outline and chapter agents."""

    def __init__(self, workspace: str):
        self.workspace = workspace
        os.makedirs(workspace, exist_ok=True)
        self.index_file = os.path.join(workspace, "index.json")
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self.index = json.load(f)
            except json.JSONDecodeError:
                self.index = self._rebuild_index()
                self._save_index()
        else:
            self.index = {"notes": [], "counter": 0}

    def _save_index(self):
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def _normalize_value(self, value: Any):
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, list):
            return [self._normalize_value(item) for item in value]
        if isinstance(value, dict):
            return {key: self._normalize_value(val) for key, val in value.items()}
        return value

    def _rebuild_index(self):
        notes = []
        counter = 0
        for filename in sorted(os.listdir(self.workspace)):
            if not (filename.startswith("note_") and filename.endswith(".md")):
                continue

            note_id = filename[:-3]
            counter = max(counter, int(note_id.split("_")[-1]))
            file_path = os.path.join(self.workspace, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            frontmatter = {}
            if frontmatter_match:
                try:
                    frontmatter = yaml.safe_load(frontmatter_match.group(1)) or {}
                except Exception:
                    frontmatter = {}

            notes.append(
                {
                    "id": note_id,
                    "title": frontmatter.get("title", note_id),
                    "note_type": frontmatter.get("note_type", "note"),
                    "tags": frontmatter.get("tags") or [],
                    "created_at": self._normalize_value(
                        frontmatter.get("created_at", datetime.now().isoformat())
                    ),
                    "updated_at": self._normalize_value(frontmatter.get("updated_at")),
                }
            )

        return {"notes": notes, "counter": counter}

    def create(self, title: str, content: str, note_type: str = "note", tags: Optional[List[str]] = None) -> str:
        self.index["counter"] += 1
        note_id = f"note_{self.index['counter']}"
        note = {
            "id": note_id,
            "title": title,
            "note_type": note_type,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
        }

        file_path = os.path.join(self.workspace, f"{note_id}.md")
        frontmatter = (
            f"---\n"
            f"title: {title}\n"
            f"note_type: {note_type}\n"
            f"tags: {json.dumps(tags or [], ensure_ascii=False)}\n"
            f"created_at: {note['created_at']}\n"
            f"---\n\n"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + content)

        self.index["notes"].append(note)
        self._save_index()
        return f"ID: {note_id}"

    def read(self, note_id: str) -> str:
        file_path = os.path.join(self.workspace, f"{note_id}.md")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        raise FileNotFoundError(f"笔记 {note_id} 不存在")

    def update(self, note_id: str, **kwargs: Any):
        file_path = os.path.join(self.workspace, f"{note_id}.md")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"笔记 {note_id} 不存在")

        content = self.read(note_id)
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if frontmatter_match:
            existing_content = content[frontmatter_match.end():]
            try:
                frontmatter: Dict[str, Any] = yaml.safe_load(frontmatter_match.group(1)) or {}
            except Exception:
                frontmatter = {}
        else:
            existing_content = content
            frontmatter = {}

        title = kwargs.get("title", kwargs.get("chapter_title"))
        if title is not None:
            frontmatter["title"] = title
        if "content" in kwargs:
            existing_content = kwargs["content"]
        if "tags" in kwargs and kwargs["tags"] is not None:
            frontmatter["tags"] = kwargs["tags"]
        if "summary" in kwargs and kwargs["summary"] is not None:
            frontmatter["tags"] = [kwargs["summary"]]
        frontmatter["note_type"] = frontmatter.get("note_type", kwargs.get("note_type", "note"))
        frontmatter["tags"] = frontmatter.get("tags") or []
        frontmatter["created_at"] = self._normalize_value(frontmatter.get("created_at"))
        frontmatter["updated_at"] = datetime.now().isoformat()

        new_frontmatter = f"---\n{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---\n\n"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_frontmatter + existing_content)

        for note in self.index["notes"]:
            if note["id"] == note_id:
                note["title"] = frontmatter.get("title", note.get("title", ""))
                note["note_type"] = frontmatter.get("note_type", note.get("note_type", "note"))
                note["tags"] = frontmatter.get("tags", note.get("tags", []))
                note["created_at"] = self._normalize_value(note.get("created_at"))
                note["updated_at"] = frontmatter["updated_at"]
                break
        self._save_index()

    def delete(self, note_id: str):
        file_path = os.path.join(self.workspace, f"{note_id}.md")
        if os.path.exists(file_path):
            os.remove(file_path)

        self.index["notes"] = [n for n in self.index["notes"] if n["id"] != note_id]
        self._save_index()
