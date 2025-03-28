import  json
from agno.tools.searxng import Searxng
from settings.config import config
def search(thinking: str, action_name: str, query: str, max_results: int):
    """
    This function is used to perform searches on the internet or the web, 
    while allowing the inclusion of necessary parameters to provide context, 
    define the action, and specify both the query and the number of search results.

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

        query (str):
            - The search query (keywords, questions, or phrases)
              to be looked up on the internet or web.

        max_results (int):
            - The maximum number of results to return,
              helping to limit the scope and improve performance of the search.

    Returns:
        A list of search results related to the given query.
    """
    search_tools = Searxng(host = config.SEARXNG_HOST, news = True)
    search_results = json.loads(search_tools.search(query, max_results= 10))
    urls = [result for result in search_results['results']]
    return str(urls)