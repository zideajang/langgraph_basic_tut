from langgraph.graph import Graph
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles


"""
对于结点引入 LLM 作为结点功能
将一问一答简单流程转换为图形式来表示
"""

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

def ask(user_input:str):
    resp = llm.invoke(user_input)
    return resp.content

def answer(resp:str):
    return f"Assistant Say: {resp}"

workflow = Graph()

workflow.add_node("ask",ask)
workflow.add_node("answer",answer)

workflow.add_edge("ask","answer")

workflow.set_entry_point("ask")
workflow.set_finish_point("answer")

app = workflow.compile()

# for output in app.stream("write hello world in python"):
#     for k,v in output.items():
#         print(f"{k=},{v=}")

# app.get_graph().print_ascii()


graph_image = app.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )
with open("graph_output.png", "wb") as f:
    f.write(graph_image)
# print(type(graph_image))
exit(0)