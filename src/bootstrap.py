import os
from dataclasses import dataclass

from dotenv import load_dotenv

from agents.chapter_generate_agent import ChapterGenerateAgent
from agents.outline_agent import OutlineAgent
from hello_agents import HelloAgentsLLM
from src.project_manager import ProjectManager


@dataclass
class AppContainer:
    project_manager: ProjectManager
    outline_agent: OutlineAgent
    chapter_agent: ChapterGenerateAgent


def build_container(workspace: str = "./outputs") -> AppContainer:
    load_dotenv()
    llm_instance = HelloAgentsLLM(
        model=os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
    )
    project_manager = ProjectManager(workspace=workspace)
    outline_agent = OutlineAgent(name="OutlineAgent", llm=llm_instance, workspace=workspace)
    chapter_agent = ChapterGenerateAgent(
        name="ChapterAgent",
        llm=llm_instance,
        workspace=workspace,
        chapter_length=3000,
    )
    return AppContainer(
        project_manager=project_manager,
        outline_agent=outline_agent,
        chapter_agent=chapter_agent,
    )
