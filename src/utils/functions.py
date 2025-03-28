from agno.models.openai import OpenAIChat
from agno.agent import Agent

def get_tool_result_summary(user_query: str,  tool_end: dict):
    agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", max_tokens = 16000, temperature=0.5),
    markdown=True,
    add_datetime_to_instructions=True
)
    prompt = f"""<your_task>
Analyze the context and tool input data. Provide brief insights about what you're doing so the user understands.
</your_task>

<user_query>
{user_query}
</user_query>

<tool_input>
{tool_end['tool_args']}
</tool_input>

<context>
{tool_end['content']}
</context>

<note>
1. Provide brief insights about the relationship between the user's query and the data being processed.
2. Mention 1-2 next steps you're taking to provide the final answer.
3. Use natural and friendly expressions, as if you're "thinking aloud" about your process.
4. Keep responses concise (2-3 sentences) but informative enough for users to understand the progress.
5. Do not include apologies, thanks, disclaimers, or follow-up questions.
6. IMPORTANT:
    - Detect the language of the user's query.
    - Respond in the language of the user's query
</note>"""
    response = agent.run(message=prompt)
    return response.content
    