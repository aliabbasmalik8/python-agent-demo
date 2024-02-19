from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor, Tool
from decouple import config
from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def search_tool(query: str) -> int:
    """Returns the results for the current event."""
    retriever = TavilySearchAPIRetriever(k=3, api_key=config('TAVILY_API_KEY'))
    results = retriever.invoke(query)
    return results

def init_agent():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=config("OPENAI_API_KEY"))

    tools = [
        Tool(
            name="WebSearch",
            func=search_tool,
            description="Useful for answering questions about current events and up-to-date general knowledge. Ask targeted questions."
        ),
        Tool(
            name="CalculateLength",
            func=get_word_length,
            description="""Useful for calculating the length of the word."""
        ),
    ]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are very powerful assistant, but don't know current events. If asked about current events use WebSearch Tool",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor