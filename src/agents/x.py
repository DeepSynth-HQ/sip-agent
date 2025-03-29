from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agents.chat.storage import storage
from agents.prompts.x import SYSTEM_PROMPT
from agents.tools.x.actions import XActionsToolkit
from agno.agent import RunResponse
from agno.utils.pprint import pprint_run_response

tools = [XActionsToolkit()]

model = OpenAIChat(id="gpt-4o-mini")
agent = Agent(
    tools=tools,
    model=model,
    storage=storage,
    system_message=SYSTEM_PROMPT,
    debug_mode=True,
)


if __name__ == "__main__":
    response: RunResponse = agent.run(
        "Reply to this tweet: https://x.com/Odin_Hoang/status/1904731233466409448 with text some jokes with media: https://www.boredpanda.com/blog/wp-content/uploads/2023/06/Cnb1RFGL6oP-png__700.jpg"
    )
    pprint_run_response(response, markdown=True)
