from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agents.chat.storage import storage
from agents.prompts.base import PROMPTS

tools = []

model = OpenAIChat(id="gpt-4o-mini")
agent = Agent(
    tools=tools,
    model=model,
    storage=storage,
    system_message=PROMPTS["x"],
    debug_mode=True,
)
