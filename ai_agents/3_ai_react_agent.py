"""
Reasoning and acting agent 

here we use the tools 

Learn how to creaste the tools in langgraph 
how to create a react graph 
work with differnt types of messages type such as tool message
 test out the robustness of our graph 
"""

from typing import Annotated ,Sequence,TypedDict
from langchain_core.messages import ToolMessage, BaseMessage,SystemMessage
from langchain_ollama import ChatOllama 
from langchain_core.tools import tool # for making tools
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode 
 

# Annotated used to add the description in the field of the 
# typedict class it is just used to add the description or lets say metadata to the field 

# sequence is used to automatically handle the stat us udpates for sequences such as by adding new messagse to a chat history 

# add_message from langgraph.graphs.message is a reducer function 
# rule that controls how updates from nodes are combined with the existing state . 
# tells us how to merge new data into the current state 

# without a reducer , updates would have , replaced the existing value entirely

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage],add_messages]



@tool
def add(a:int,b:int)->int : 
    """This is an addition function that adds two numbers together """
    return a+b

@tool
def multiply(a:int,b:int)->int : 
    """This is an addition function that multiplies two numbers together """
    return a*b

@tool
def subtract(a:int,b:int)->int : 
    """This is an addition function that ads two numbers together """
    return a-b

tools = [add,multiply,subtract]

model = ChatOllama(model='qwen2.5:3b-instruct-q4_0').bind_tools(tools)

def model_call(state:AgentState)->AgentState:
    system_prompt = SystemMessage(content='You are my ai assistant , please answer my query to the best of your ability')
    response = model.invoke([system_prompt]+state['messages'])
    return {"messages":[response]}


def should_continue(state:AgentState)->AgentState:
    """Decide wheather to continue or exit"""
    messages = state['messages']
    last_message = messages[-1]

    if not last_message.tool_calls:

        return "end"
    else :
        return "continue"


graph = StateGraph(AgentState)

graph.add_node("our_agent",model_call)

# making tool node for the app

tool_node = ToolNode(tools=tools)


graph.add_node("tools",tool_node)


graph.set_entry_point("our_agent")


graph.add_conditional_edges(
"our_agent",
should_continue, # node  for routing 
{
    "continue":"tools",
    "end":END
}

)

graph.add_edge("tools","our_agent")

app = graph.compile()


def print_stream(stream):
    for s in stream :
        message = s['messages'][-1]
        if isinstance(message,tuple):
            print(message)
        else : 
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))