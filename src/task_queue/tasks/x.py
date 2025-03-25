from typing import List
from task_queue.celery_app import app


@app.task(name="tasks.x.create_post")
def create_tweet(text: str, medias: List[str]) -> None:
    pass


@app.task(name="tasks.x.reply_to_tweet")
def reply_to_tweet(text: str, tweet_id: str, username: str) -> None:
    pass
