import datetime

from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph


def add_hey(input: list[HumanMessage]):
    input[0].content = input[0].content + " hey"
    return input

def add_time(input: list[HumanMessage]):
    input[0].content = input[0].content + f" {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"

def add_message(input:list[HumanMessage]):
    input[0].content = input[0].content + f" send some message"

graph = MessageGraph()

graph.add_node("add_hey", add_hey)
graph.add_edge("add_hey", "add_time")
graph.add_edge("add_hey", "add_message")

graph.add_node("add_time", add_time)
graph.add_node("add_message", add_message)

graph.add_edge("add_time", "final_node")
graph.add_edge("add_message", "final_node")

graph.add_node("final_node", add_hey)
graph.add_edge("final_node", END)

graph.set_entry_point("add_hey")

app = graph.compile()

app.get_graph().print_ascii()

res = app.invoke("hello")
print(res)