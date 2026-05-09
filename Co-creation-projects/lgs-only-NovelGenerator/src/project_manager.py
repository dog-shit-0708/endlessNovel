import json
import os


class ProjectManager:
    def __init__(self, workspace: str = "./outputs"):
        self.workspace = workspace
        os.makedirs(workspace, exist_ok=True)

    def get_project_dir(self, title: str, novel_id: str) -> str:
        return os.path.join(self.workspace, f"{title}-{novel_id}")

    def get_mapping_file(self, title: str, novel_id: str) -> str:
        return os.path.join(self.get_project_dir(title, novel_id), "project_data.json")

    def load_mapping(self, title: str, novel_id: str):
        path = self.get_mapping_file(title, novel_id)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"novel_id": novel_id, "title": title, "outline_id": None, "chapters": []}

    def save_mapping(self, title: str, novel_id: str, data):
        path = self.get_mapping_file(title, novel_id)
        os.makedirs(self.get_project_dir(title, novel_id), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def update_outline_mapping(self, title: str, novel_id: str, outline_id: str):
        data = self.load_mapping(title, novel_id)
        data["outline_id"] = outline_id
        self.save_mapping(title, novel_id, data)

    def add_chapter_mapping(self, title: str, novel_id: str, chapter_data):
        data = self.load_mapping(title, novel_id)
        data["chapters"].append(chapter_data)
        self.save_mapping(title, novel_id, data)

    def update_chapter_mapping(self, title: str, novel_id: str, note_id: str, update_data):
        data = self.load_mapping(title, novel_id)
        for chapter in data["chapters"]:
            if chapter["id"] == note_id:
                chapter.update(update_data)
                break
        self.save_mapping(title, novel_id, data)

    def remove_chapter_mapping(self, title: str, novel_id: str, note_id: str):
        data = self.load_mapping(title, novel_id)
        data["chapters"] = [c for c in data["chapters"] if c["id"] != note_id]
        self.save_mapping(title, novel_id, data)
