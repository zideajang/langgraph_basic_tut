import operator
from typing import Annotated, Sequence, TypedDict

from rich.console import Console

from langchain_core.messages import SystemMessage

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage

from langgraph.graph import END, StateGraph, START

console = Console()

# config
model_llama = ChatOllama(model="llama3.1")
model_gemma = ChatOllama(model="gemma2")

models = {
    "llama": model_llama,
    "gemma": model_gemma
}

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


def _call_model(state,config):
    model_name = config["configurable"].get("model","llama")
    messages = state["messages"]
    console.print(model_name)
    if "system_message" in config["configurable"]:
        messages = [
            SystemMessage(content=config["configurable"]["system_message"])
        ] + messages
    m =  models[model_name]
    response = m.invoke(state["messages"])
    return {"messages": [response]}
# def _call_model(state,config):
#     m = models[config["configurable"].get("model", "llama")]
#     response = m.invoke(state["messages"])
#     return {"messages": [response]}


# Define a new graph
workflow = StateGraph(AgentState)

workflow.add_node("model", _call_model)

workflow.add_edge(START, "model")
workflow.add_edge("model", END)

app = workflow.compile()
config = {"configurable": {"system_message": "以中文回复"}}
resp = app.invoke({"messages": [HumanMessage(content="你好")]},config=config)
console.print(resp)
exit(0)
# config = {"configurable": {"model": "gemma"}}


# resp = app.invoke({"messages": [HumanMessage(content="hi")]})
resp = app.invoke({"messages": [HumanMessage(content="你好")]},config=config)

for msg in resp['messages']:
    if isinstance(msg,HumanMessage):
        console.print(f":boy: {msg.content}")
    else:
        console.print(f":robot: {msg.content}")