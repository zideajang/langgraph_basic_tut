from typing import Any
from langgraph.graph import Graph
from langchain_community.chat_models import ChatOllama

from rich.console import Console
from rich.markdown import Markdown

console = Console()

# state = {
#     "user_ask":"write hello world in python",
#     "ai_answer":""
# }

class AskNode:
    def __init__(self) -> None:
        self.llm = ChatOllama(
            model="llama3.1",
            temperature=0,
        )

    def __call__(self, state) -> Any:
        resp = self.llm.invoke(state["user_ask"])
        return {
            "user_ask":state["user_ask"],
            "ai_answer":resp.content
        }

class AnswerNode:
    def __call__(self,state) -> Any:
        print(state)
        return state
    

workflow = Graph()

workflow.add_node("ask",AskNode())
workflow.add_node("answer",AnswerNode())

workflow.add_edge("ask","answer")

workflow.set_entry_point("ask")
workflow.set_finish_point("answer")

app = workflow.compile()

for output in app.stream({"user_ask":"write hello world in python"}):
    for k,v in output.items():
        console.print(f" node: {k} ",style="white on blue")
        console.print("\n")
        console.print(Markdown(v['ai_answer']))
        console.print("--"*50)

        # print(f"{k=},{v=}")