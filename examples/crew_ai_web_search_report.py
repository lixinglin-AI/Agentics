from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # For Stdio Server
import os
from crewai import Agent, Task, Crew
from agentics.core.llm_connections import get_llm_provider
from pydantic import BaseModel, Field
from typing import Optional
import yaml

class Citation(BaseModel):
    url: Optional[str] = None
    authors: Optional[list[str]] = None
    title:Optional[str] = None
    relevant_text:Optional[str] = None

class WebSearchReport(BaseModel):
    "This is the report of a web search in which a question is answered after extensive web search"
    title: Optional[str] = None
    abstract: Optional[str] = None
    full_report: Optional[str]=Field(None,
        description="""Markdown reporting full report of the findings made from web search.""")
    citations: list[Citation] = Field([],description="Citations to relevant sources")
    
fetch_params=StdioServerParameters(
    command="uvx",
    args=["mcp-server-fetch"],
    env={"UV_PYTHON": "3.12", **os.environ},
)
search_params=StdioServerParameters(
    command="python3",
    args=[os.getenv("MCP_SERVER_PATH")],
    env={"UV_PYTHON": "3.12", **os.environ},
)
with MCPServerAdapter(fetch_params) as fetch_tools, \
     MCPServerAdapter(search_params) as search_tools:

    print(f"Available tools from Stdio MCP server: {[tool.name for tool in fetch_tools]}")
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in search_tools]}")
    tools=fetch_tools + search_tools

    doc_agent = Agent(
        role="Doc Searcher",
        goal="Find answers to questions from the user using the available MCP tool.",
        backstory="A helpful assistant for extensive web search reports.",
        tools=tools,
        reasoning=True,
        reasoning_steps=10,
        memory=True,
        verbose=True,
        llm=get_llm_provider("gemini")
    )

    doc_task = Task(
        description="""Your task is to perform an extensive web search about
        the following question {question} and return a document providing answers to 
        the questions that explore several interesting aspects, each of them supported 
        by pertinent information from web search.  """,
        expected_output="""A structured document in which each section answer a specific aspect of the question.
        in a very detailed and accurate manner. Please include supporting passages to justify it""",
        agent=doc_agent,
        output_pydantic=WebSearchReport,
        markdown=True
    )

    crew = Crew(
        agents=[doc_agent],
        tasks=[doc_task],
        #verbose=True,
        memory=True
    )

    result = crew.kickoff(inputs={"question": "Make a literature report on Large Language Models from arxiv" })
    print(yaml.dump(result.pydantic.model_dump(), sort_keys=False))