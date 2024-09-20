from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph

"""
选择性结点
"""

# 功能
def entry(input: list[HumanMessage]):
    return input


def one_task(input: list[HumanMessage]):
    print("working with one task")
    return input


def two_task(input: list[HumanMessage]):
    print("working with two task")
    return input


def router(input: list[HumanMessage]):
    if "two task" in input[0].content:
        return "two_task"
    else:
        return "one_task"


graph = MessageGraph()

graph.add_node("plan", entry)
graph.add_node("two_task", two_task)
graph.add_node("one_task", one_task)

graph.add_conditional_edges(
    "plan", router, {"two_task": "two_task", "one_task": "one_task"}
)
graph.add_edge("two_task", END)
graph.add_edge("one_task", END)

graph.set_entry_point("plan")

runnable = graph.compile()

runnable.invoke("I want to two task")