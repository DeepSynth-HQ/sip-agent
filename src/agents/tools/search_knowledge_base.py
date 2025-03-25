from settings.config import config
from settings.log import logger
from langchain_openai import OpenAIEmbeddings
import pandas as pd
from qdrant_client import QdrantClient

def search_knowledge_base(self, thinking: str, action_name: str, queries: list[str]):
        """
        Get documents from the vector database for the campaign. Or related terminologies about the campaign
        Args:
            thinking (str):
                - Natural, human-like thought process analyzing the user query.
                - Reflects internal reasoning as if speaking to oneself, with a conversational tone.
                - Should include analysis of what the user is asking for and why.
                - Each new thinking section must continue the logic from the previous thinking section (if any), without repeating content that has already been thought through.
                - Subsequent thinking sections need to continue the thought process from where the previous thinking section ended, developing ideas or moving to the next step in the thought chain.
                - Concludes with decision statements like "Okay, now I will..." or "I should..."
                - Demonstrates the reasoning path from query to chosen action.
                - Written in first-person perspective as if the model is thinking aloud.
                - MOST IMPORTANT:
                   + Detect the language used in the user's message/input/query or request.
                   + Return your response in the user's language
                   
            action_name (str):
                - Detailed noun phrase in natural language describing exactly what action is being performed.
                - Clearly states both the action and specific object
                - Indicates the purpose of the action and the type of data/information being processed.
                - Sufficiently detailed for readers to understand precisely what action is being performed.
                - MOST IMPORTANT:
                    + Detect the language used in the user's message/input/query or request.
                    + Return your response in the user's language
                                
            queries (list[str]): 
                - Standard alone queries created from user requests to be used for querying, searching for information

        Returns:
            list: list of documents
        """
        logger.info(f"queries response: {queries}")
        if not queries:
            return []
        logger.info(f"Queries: {queries}")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", api_key=config.OPENAI_API_KEY
        )
        final_docs = []
        for query in queries[:5]:
            print(f"RETRIEVE TO {query.campaign_name} database")
            try:
                client = QdrantClient(url=config.QDRANT_URI, api_key=config.QDRANT_API_KEY, port=443)
                hits = client.query_points(
                    collection_name="story_protocol",
                    query=embeddings.embed_query( query),
                    limit=3,
                    score_threshold = 0.3
                ).points
                for hit in hits:
                    final_docs.append(hit.payload)
            except Exception as e:
                print("Error:     {e}")
                pass
        if final_docs:
            final_docs = sorted(final_docs, key=lambda doc: (doc['file_id'], doc['chunk_index']))
        return final_docs
