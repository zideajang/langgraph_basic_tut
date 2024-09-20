import datetime
from rich.console import Console

from typing import Literal

from langchain_core.messages import AIMessage,ToolMessage
from langchain_core.tools import tool

from langchain_experimental.llms.ollama_functions import OllamaFunctions
# 
from langgraph.prebuilt import ToolNode

from langgraph.graph import StateGraph, MessagesState

console = Console()

@tool
def get_weather(location:str):
    """Call to get the current weather."""
    if location.lower() == "shenyang":
        return "It's 30 degreen and sunny"
    else:
        return "It's 28 degreen and cloudy"
    

@tool
def get_current_time():
    """Get current time """
    return datetime.datetime.now()

# console.print(get_current_time.name)
# console.print(get_current_time.description)

tools = [get_weather,get_current_time]
tool_node = ToolNode(tools)

# 调用大语言模型 chat HumanMessage(role="user",content="")
# 大语言模型返回 AIMessage(role="ai",content="",tool_calls=)
message_with_single_tool_call = AIMessage(
    content="",
    tool_calls = [
        {
            "name":"get_weather",
            "args":{"location":"shenyang"},
            "id":"tool_call_id",
            "type":"tool_call"
        }
    ]
)

# AIMessage tool_calls 

# resp = tool_node.invoke({"messages": [message_with_single_tool_call]})
# print(resp)
# console.print(resp)

# exit(0)

# [b zhan],  {"id":  zidea2015,"tutorial " langchain 快速入门": 9.9 RMB 


message_with_multiple_tool_calls = AIMessage(
    content="",
    tool_calls = [
        {
            "name":"get_current_time",
            "args":{},
            "id":"tool_call_id_1",
            "type":"tool_call"
        },
        {
            "name":"get_weather",
            "args":{"location":"shenyang"},
            "id":"tool_call_id_2",
            "type":"too_call"
        }
    ]
)

resp = tool_node.invoke({"messages": [message_with_multiple_tool_calls]})
console.print(resp)
exit(0)


llm = OllamaFunctions(
    base_url="http://127.0.0.1:11434",
    model="llama3.1", 
    format="json")

model_with_tools  = llm.bind_tools(tools)


resp = model_with_tools.invoke("what's the weather in shenyang")

console.print(resp.tool_calls)

# ReAct Agent


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"

def call_model(state: MessagesState):
    # for msg in messages:
    #     if isinstance(msg,ToolMessage):
            

    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge("__start__", "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", "agent")

app = workflow.compile()

for chunk in app.stream(
    {"messages":[("human","what's the weather in shenyang?")]},
    stream_mode="values"):
    chunk["messages"][-1].pretty_print()