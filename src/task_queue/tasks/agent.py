from celery import shared_task
from agents.x import agent
from pydantic import BaseModel
from textwrap import dedent
from agno.agent import RunResponse


@shared_task(name="tasks.agent.call_to_reply_to_mentions", queue="agent")
def call_to_reply_to_mentions(tweet_id: str, text: str, username: str, name: str):
    response: RunResponse = agent.run(
        dedent(
            f"""
            [RULES]: You are me, a human.
            [CONTEXT]: {username} mentioned you in a tweet (https://x.com/{username}/status/{tweet_id}) with the following text: {text} 
            [TASK]: Reply {name} by your thoughts. 
            
        """
        )
    )
    return response.content
