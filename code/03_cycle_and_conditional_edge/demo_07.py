from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from langchain_community.chat_models import ChatOllama

"""
带有环的图
"""

model = ChatOllama(model="llama3.1",temperature=0)

def entry(input: list[HumanMessage]):
    return input

def action(input: list[HumanMessage]):
    print("Action taken:", [msg.content for msg in input])
    if len(input) > 5:
        input.append(HumanMessage(content="end"))
    else:
        input.append(HumanMessage(content="continue"))
    return input


def should_continue(input: list):
    last_message = input[-1]
    if "end" in last_message.content:
        return "__end__"
    return "action"


graph = MessageGraph()

graph.add_node("agent", entry)
graph.add_node("action", action)

graph.add_conditional_edges(
    "agent", should_continue, {"action": "action", "__end__": END}
)
graph.add_edge("action", "agent")

graph.set_entry_point("agent")

app = graph.compile()

app.invoke("hell cycle")