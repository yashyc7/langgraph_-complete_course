from langgraph.graph import StateGraph,END
import random 
from typing import Dict,List,TypedDict

class AgentState(TypedDict):
    name:str
    number : List[int]
    counter : int 

# lets build the node now 

def greeting_node(state : AgentState)->AgentState : 
    """
    Greeting node which says hi to the person
    """
    state['name']=f'Hi there {state["name"]}'

    state['counter']=0 

    return state

def random_node(state:AgentState)->AgentState:
    """
    geenrate a random number from 0 to 10 

    """

    state["number"].append(random.randint(0,10))
    state['counter']+= 1 
    return state  


def should_continue(state:AgentState)->AgentState:
    """function to decide what to do next"""
    if state['counter']<5 : 
        print("entering loop ",state['counter'])
        return 'loop'
    else:
        return "exit"

graph = StateGraph(AgentState)

graph.add_node("greeting",greeting_node)
graph.add_node("random",random_node)
graph.add_edge("greeting","random")


graph.add_conditional_edges(
    "random", # source node 
    should_continue, # routing function

    {
        "loop":'random',
        "exit":END
    }

)
 
graph.set_entry_point("greeting")

app = graph.compile()

print(app.get_graph().draw_mermaid())

print(app.invoke({"name":"yash","number":[],"counter":-100}))


# entering loop  1
# entering loop  2
# entering loop  3
# entering loop  4
# {'name': 'Hi there yash', 'number': [9, 3, 5, 10, 9], 'counter': 5}