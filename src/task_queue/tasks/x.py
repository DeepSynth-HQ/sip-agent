from typing import List
from task_queue.celery_app import app


@app.task(name="tasks.x.create_tweet")
def create_tweet(text: str, media_paths: List[str]): ...


@app.task(name="tasks.x.reply_to_tweet")
def reply_to_tweet(text: str, tweet_id: str, username: str, media_paths: List[str]): ...


@app.task(name="tasks.x.get_mentions")
def get_mentions(): ...


@app.task(name="tasks.x.prepare_reply_to_mentions")
def prepare_reply_to_mentions(): ...
