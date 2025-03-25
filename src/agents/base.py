from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agents.tools import StoryProtocolTool

tools = [StoryProtocolTool()]

model = OpenAIChat(id="gpt-4o-mini")
agent = Agent(tools=tools, model=model)
