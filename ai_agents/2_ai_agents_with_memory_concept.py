"""
Use differnt message types human message and ai messasge 
maintain a full converstaion history using both message types 
use local ai model using langchain's ollama
create a sophisticated conversattion loop  
"""
import os 
from typing import List,Union,TypedDict
from langchain_core.messages  import AIMessage , HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph,START,END

#insteead of doing this thing we can use the union below 
# class AgentState(TypedDict):
#     messages : List[HumanMessage]
#     ai_messages : List[AIMessage]

# we can use the union right here 

class AgentState(TypedDict):
    messages : List[Union[AIMessage,HumanMessage]]

    #human message is datatype in langchain  , langgraph 
    # allows me to store the either the human message or the ai messages 

llm = ChatOllama(model='qwen2.5:3b-instruct-q4_0')

def process(state:AgentState)->AgentState:
    """
    This node will solve the request you input 
    """

    response = llm.invoke(state["messages"])

    state['messages'].append(AIMessage(response.content))
    print(f"\n AI : {response.content}")

    return state

graph = StateGraph(AgentState)

graph.add_node("process",process)

graph.add_edge(START,"process")
graph.add_edge("process",END)

agent = graph.compile()

converstational_history = [] # for memory setup 

user_input = input("Enter: ")

while user_input!="exit":
    converstational_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages":converstational_history})

    # print(result['messages'])
 
    converstational_history = result["messages"]  
    
    user_input = input("Enter:")

with open("logging.txt","w") as file : 
    file.write ("Your conversation log \n ")
    for message in converstational_history: 
        if isinstance(message,HumanMessage):
            file.write(f"You: {message.content} \n")
        elif isinstance(message,AIMessage):
            file.write(f"AI : {message.content} \n\n")
    file.write("End of conversation")

print("conversation stored to logging.txt")



