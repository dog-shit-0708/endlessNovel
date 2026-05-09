import os
import sys
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../agents")))

from src.bootstrap import build_container

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OutlineRequest(BaseModel):
    novel_id: str
    title: str
    user_input: str
    tags: List[str] = Field(default_factory=list)
    target_length: Optional[int] = 3000
    style_tags: Dict[str, str] = Field(default_factory=dict)
    is_fanfic: bool = False
    work_name: Optional[str] = None
    main_characters: List[str] = Field(default_factory=list)


class OutlineUpdateRequest(BaseModel):
    novel_id: str
    title: str
    note_id: str
    content: str
    tags: Optional[List[str]] = None


class ChapterGenerateRequest(BaseModel):
    novel_id: str
    title: str
    user_input: str
    num_chapters: int = 1
    chapter_length: int = 3000
    is_fanfic: bool = False
    work_name: Optional[str] = None
    main_characters: List[str] = Field(default_factory=list)


class ChapterUpdateRequest(BaseModel):
    novel_id: str
    title: str
    note_id: str
    content: Optional[str] = None
    chapter_title: Optional[str] = None
    summary: Optional[str] = None
    next_chapter_prediction: Optional[str] = None


container = build_container(workspace="./outputs")
project_manager = container.project_manager
outline_agent = container.outline_agent
chapter_agent = container.chapter_agent


@app.get("/projects/{title}/{novel_id}")
def get_project_data(title: str, novel_id: str):
    return project_manager.load_mapping(title, novel_id)


@app.get("/fanfic/context/{work_name}")
def get_fanfic_context(work_name: str, main_characters: Optional[str] = None):
    character_names = [item.strip() for item in main_characters.split(",")] if main_characters else None
    context = outline_agent.canon_manager.get_structured_context(work_name, None, character_names)
    if not context:
        raise HTTPException(status_code=404, detail="Fanfic context not found")
    return {
        "work": context["work"].__dict__,
        "characters": [item.__dict__ for item in context["characters"]],
        "relationships": [item.__dict__ for item in context["relationships"]],
    }


@app.post("/outline/generate")
def generate_outline(req: OutlineRequest):
    run_kwargs = {
        "novel_id": req.novel_id,
        "title": req.title,
        "target_length": req.target_length,
        "is_fanfic": req.is_fanfic,
        "work_name": req.work_name,
        "main_characters": req.main_characters,
    }
    run_kwargs.update(req.style_tags)
    response, note_id = outline_agent.run(req.user_input, **run_kwargs)
    project_manager.update_outline_mapping(req.title, req.novel_id, note_id)
    return {"note_id": note_id, "content": response}


@app.get("/outline/{title}/{novel_id}/{note_id}")
def get_outline(title: str, novel_id: str, note_id: str):
    content = outline_agent.get_outline(novel_id, note_id, title=title)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()
    return {"content": content}


@app.put("/outline/update")
def update_outline(req: OutlineUpdateRequest):
    outline_agent.update_outline(req.novel_id, req.note_id, title=req.title, content=req.content, tags=req.tags)
    return {"status": "success"}


@app.delete("/outline/delete")
def delete_outline(novel_id: str, title: str, note_id: str):
    outline_agent.del_outline(novel_id, note_id, title=title)
    data = project_manager.load_mapping(title, novel_id)
    if data["outline_id"] == note_id:
        data["outline_id"] = None
        project_manager.save_mapping(title, novel_id, data)
    return {"status": "success"}


@app.post("/chapter/generate")
def generate_chapters(req: ChapterGenerateRequest):
    generated_chapters = []
    current_input = req.user_input
    for i in range(req.num_chapters):
        try:
            chapter_data, note_id = chapter_agent.run(
                user_input=current_input,
                novel_id=req.novel_id,
                novel_title=req.title,
                chapter_length=req.chapter_length,
                is_fanfic=req.is_fanfic,
                work_name=req.work_name,
                main_characters=req.main_characters,
            )
            if i == 0:
                current_input = ""
            chapter_info = {
                "id": note_id,
                "title": chapter_data.get("title", "Unknown"),
                "summary": chapter_data.get("summary", ""),
            }
            generated_chapters.append(chapter_info)
            project_manager.add_chapter_mapping(req.title, req.novel_id, chapter_info)
        except Exception as e:
            print(f"Error generating chapter {i + 1}: {e}")
            break
    return {"generated_chapters": generated_chapters}


@app.get("/chapter/{title}/{novel_id}/{note_id}")
def get_chapter(title: str, novel_id: str, note_id: str):
    path = os.path.join("./outputs", f"{title}-{novel_id}", "chapters", f"{note_id}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        return {"content": content}
    raise HTTPException(status_code=404, detail="Chapter not found")


@app.put("/chapter/update")
def update_chapter(req: ChapterUpdateRequest):
    update_kwargs = {}
    if req.content is not None:
        update_kwargs["content"] = req.content
    if req.chapter_title is not None:
        update_kwargs["title"] = req.chapter_title
    if req.summary is not None:
        update_kwargs["summary"] = req.summary
    if req.next_chapter_prediction is not None:
        update_kwargs["next_chapter_prediction"] = req.next_chapter_prediction

    chapter_agent.update_chapter(req.novel_id, req.note_id, novel_title=req.title, **update_kwargs)

    mapping_update = {}
    if req.chapter_title:
        mapping_update["title"] = req.chapter_title
    if req.summary:
        mapping_update["summary"] = req.summary
    if mapping_update:
        project_manager.update_chapter_mapping(req.title, req.novel_id, req.note_id, mapping_update)
    return {"status": "success"}


@app.delete("/chapter/delete")
def delete_chapter(novel_id: str, title: str, note_id: str):
    chapter_agent.del_chapter(novel_id, note_id, novel_title=title)
    project_manager.remove_chapter_mapping(title, novel_id, note_id)
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
