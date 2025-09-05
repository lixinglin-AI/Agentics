from crewai import Agent, Task, Crew, Process

from crewai.tools import tool
from ddgs import DDGS



from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # For Stdio Server
import os
from agentics.core.llm_connections import get_llm_provider

# StdioServerParameters(
#     command="uvx",
#     args=["mcp-server-fetch"],
#     env={**os.environ},
# )
server_params=StdioServerParameters(
    command="uvx",
    args=["mcp-server-fetch"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

## Define a Crew AI tool to get news for a given date using the DDGS search engine
@tool("fetch_data_async")
def web_search(query: str) -> str:
    """ Fetch web search results for the given query using DDGS."""
    return str(DDGS().text(query, max_results=10))    

with MCPServerAdapter(server_params) as server_tools:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in server_tools]}")

    # Create a conversational agent with a friendly role/goal
    chat_agent = Agent(
        role="Helpful Assistant",
        goal="Have a natural multi-turn conversation",
        backstory="You are a friendly assistant that remembers context and asks for clarification when needed.",
        memory=True  # enable memory for conversational context
    )

    # Define a simple Task that represents a single AI response
    task = Task(
        description="Respond appropriately to user's message, maintaining context. {input}",
        expected_output="A conversational reply",
        agent=chat_agent,
        tools=[web_search] + server_tools
    )

    crew = Crew(
        agents=[chat_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
        memory=True,  # ensure conversation state persists across turns
    )

    # Example conversation loop
    while user_input := input("You: ").strip():
        result = crew.kickoff(inputs={"input": user_input})
        print("Assistant:", result)