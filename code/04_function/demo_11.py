from langgraph.graph import Graph
from langchain_community.chat_models import ChatOllama
from rich.console import Console
from rich.markdown import Markdown

console = Console()
# 大语言模型
model = ChatOllama(
    model="llama3.1",
    temperature=0,
)

class OpenWeatherMapAPIWrapper:
    def run(self,city_name):
        # print(city_name)
        if city_name.lower() == "shenyang":
            return "tempature:30"

AgentState = {}
AgentState["messages"] = []

def function_1(state):
    messages = state['messages']
    user_input = messages[-1]
    complete_query = "Your task is to provide only the city name based on the user query. \
Nothing more, just the city name mentioned. Following is the user query: " + user_input
    response = model.invoke(complete_query)
    state['messages'].append(response.content)  # appending AIMessage response to the AgentState
    return state

def function_2(state):
    messages = state['messages']
    agent_response = messages[-1]
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run(agent_response)
    state['messages'].append(weather_data)
    return state

def function_3(state):
    messages = state['messages']
    user_input = messages[0]
    available_info = messages[-1]
    
    agent2_query = "Your task is to provide info concisely based on the user query an the available information from the internet. Following is the user query: " + user_input + " Available information: " + available_info
    
    response = model.invoke(agent2_query)
    messages.append(response.content)
    return {"messages":messages}

workflow = Graph()

workflow.add_node("agent",function_1)
workflow.add_node("tool",function_2)
workflow.add_node("responder",function_3)

workflow.add_edge("agent","tool")
workflow.add_edge("tool","responder")

workflow.set_entry_point("agent")
workflow.set_finish_point("responder")

app = workflow.compile()

inputs = {
    "messages":["what is the temperature in shenyang"]
}

# app.invoke(inputs)


for output in app.stream(inputs):
    for k,v in output.items():
        console.print(f" node: {k} ",style="white on blue")
        console.print("\n")
        for message in v['messages']:
            console.print(Markdown(message))
        console.print("--"*20)