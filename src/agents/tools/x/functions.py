from typing import List, Optional
from pydantic import BaseModel
from task_queue.tasks.x import (
    create_tweet as create_tweet_task,
    reply_to_tweet as reply_to_tweet_task,
)
from settings.log import logger


class XFunctions:
    @staticmethod
    def create_tweet(text: str, media_paths: List[str] = []):
        """
        Create a new X post

        Args:
            text (str): The text of the post
            media_paths (List[str]): The media of the post, It should be a list of image paths

        Returns:
            Task: The task that creates the tweet
        """
        task = create_tweet_task.delay(text, media_paths)
        result = task.get()
        logger.info(f"[🚩] Created tweet task: {result}")
        return str(result)

    @staticmethod
    def reply_to_tweet(text: str, tweet_id: str, username: str, media_paths: List[str]):
        """
        Reply to an existing X post

        Args:
            text (str): The text of the reply
            tweet_id (str): The id of the tweet to reply to
            username (str): The username of the tweet to reply to
            media_paths (List[str]): The media of the reply, It should be a list of image paths
        Returns:
            Task: The task that replies to the tweet
        """
        task = reply_to_tweet_task.delay(text, tweet_id, username, media_paths)
        result = task.get()
        logger.info(f"[🚩] Created reply task: {result}")
        return str(result)
