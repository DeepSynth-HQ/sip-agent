from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat

tools = []

model = OpenAIChat(model="gpt-4o-mini")
agent = Agent(tools=tools, model=model)
