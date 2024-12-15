import os
import yaml

import asyncio

from rich.console import Console

from typing import Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from langchain_groq import ChatGroq
from langchain_experimental.llms.ollama_functions import OllamaFunctions

console = Console()

# stream
# values
# updates

def get_config():
    with open("D:/config.yaml","r") as file:
        config = yaml.safe_load(file)
    return config

config = get_config()
os.environ['GROQ_API_KEY'] = config['GROQ_API_KEY']


@tool
def get_weather(city: Literal["shenyang", "dalian"]):
    """Use this to get weather information."""
    if city.lower() == "shenyang":
        return "It's always sunny in shenyang"
    else:
        raise AssertionError("Unknown city")
    
tools = [get_weather]
model = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview")
# model = OllamaFunctions(
#     base_url="http://127.0.0.1:11434",
#     model="llama3.1", 
#     format="json"
#     )

graph = create_react_agent(model, tools)


inputs = {"messages": [("human", "what's the weather in shenyang")]}

async def main():
    # values or updates 
    async for event,chunk in graph.astream(inputs, stream_mode=["updates","debug"]):
        console.print(f"Receiving new event of type: {event}...",style="white on blue")
        console.print(chunk)
        console.print("\n\n")

if __name__ == "__main__":
   asyncio.run(main())