
import json
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agents.tools import StoryProtocolTool
from agents.chat.storage import storage
from agents.prompts.base import PROMPTS
from agents.tools.search_knowledge_base import search_knowledge_base
from agents.tools.web_crawler import webpage_crawler
from agents.tools.web_search import search
from agno.storage.agent.mongodb import MongoAgentStorage
from settings.config import config
from agno.utils.log import logger
from utils.functions import get_tool_result_summary
class MetapoolAgent:

    def __init__(self, user_id: str, session_id: str):
        self.storage = MongoAgentStorage(
            collection_name="storage_agent", db_url=config.MONGO_URI, db_name="agent"
        )
        self.user_id = user_id
        self.session_id = session_id
        
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini", temperature=0.3, max_tokens=16000),
            tools=[StoryProtocolTool(), search_knowledge_base, webpage_crawler, search ],
            add_history_to_messages=True,
            num_history_responses=6,
            debug_mode=True,
            storage=self.storage,
            session_id=self.session_id,
            user_id=self.user_id,
            read_chat_history=True,
            markdown=True,
            add_datetime_to_instructions=True,
        )

        self._init_context()

    def _init_context(self):
        user_id = self.user_id
        username ="Phúc Tính"
        logger.info(f"username: {username}")
        logger.info(f"user_id: {user_id}")
        self.agent.context = {
            "user_id": user_id,
            "username": username
        }

    
    def run(self, message: str, stream: bool = True, stream_intermediate_steps= True):
        if stream:
            
            response = self.agent.run(message, stream=stream, stream_intermediate_steps=stream_intermediate_steps)
            for chunk in response:
                if chunk.event == "ToolCallStarted":
                    chunk.content_type="tool_start"
                    chunk.content = json.loads(chunk.model_dump_json())['tools'][-1]
                if chunk.event == "ToolCallCompleted":
                    chunk.content_type="tool_end"
                    chunk.content = get_tool_result_summary(user_query = message, tool_end = json.loads(chunk.model_dump_json())['tools'][-1]) #json.loads(chunk.model_dump_json())['tools'][-1]
                if chunk.event == "RunResponse":
                    chunk.content_type = "answer"
                yield chunk 
                
        else:

            response = self.agent.run(message, stream=False)
            return response



if __name__ == "__main__":
    import uuid
    user_id = "6797449f4951faf1a1ff306c"
    session_id = str(uuid.uuid4())
    print("session id:    ", session_id)
    while True:
        message = input("\n💫: ")
        agent = MetapoolAgent(user_id, session_id)
        response = agent.run(message=message, stream=True, stream_intermediate_steps=True)
        answer = ""
        for chunk in response:
                if chunk.content_type == "tool_start":
                    chunk_content =chunk.content
                    print("ACTION NAME:    \n", chunk_content['tool_args']['action_name'])
                    print("THINKING:    \n", chunk_content['tool_args']['thinking'])
                if chunk.content_type == "tool_end":
                    chunk_content = chunk.content
                    print("content:    \n", chunk_content)
        # print("=============== ANSWER =======================\n", answer)
        # print("History:     \n", [m.model_dump(include={"role", "content"}) for m in agent.agent.memory.messages])
