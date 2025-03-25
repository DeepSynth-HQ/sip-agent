from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agents.tools import StoryProtocolTool
from agents.chat.storage import storage
from agents.prompts.base import PROMPTS
from agents.tools.search_knowledge_base import search_knowledge_base
tools = [StoryProtocolTool(), search_knowledge_base]

model = OpenAIChat(id="gpt-4o-mini")
agent = Agent(
    tools=tools,
    model=model,
    storage=storage,
    system_message=PROMPTS["base"],
    debug_mode=True,
)
