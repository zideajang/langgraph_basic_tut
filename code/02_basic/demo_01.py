from langgraph.graph import Graph

"""
func_1(input) -> func_2(output_func_1)->output

设计节点和边
- 定义节点 node
- 用边将节点连接 edge
指定 start 和 end 节点

"""


# 定义节点功能(逻辑)
def func_1(input_1):
    return f"{input_1} hey"

def func_2(input_2):
    return f"{input_2} hello"

# 构建图
# node_1 -> node_2
workflow = Graph()

workflow.add_node("node_1",func_1)
workflow.add_node("node_2",func_2)

workflow.add_edge("node_1","node_2")

workflow.set_entry_point("node_1")
workflow.set_finish_point("node_2")

# 对图进行编译
app = workflow.compile()

# 调用方式
# res = app.invoke("user input some word")
# print(res)
# exit(0)
# print(res)

for output in app.stream("user input some word"):
    for k,v in output.items():
        print(f"{k=},{v=}")
