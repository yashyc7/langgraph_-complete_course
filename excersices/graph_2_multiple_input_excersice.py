"""
create a grpah where you pass in a single list of integres along
with a name and an operation is a "+"  you add the elements and if it is a 
" * " , you multiply the elementes all within the same node 
input : {"name":"jack sparrow" , "values ": [1,2,3,4],"opereation" : "*" }

Output : " Hi jack sparrow your answer is 24" 

"""

from langgraph.graph import StateGraph
from typing import TypedDict, List 
import operator 
import functools 

class AgentState(TypedDict): 
    name : str
    values: List[int]
    operator : str
    result : str

# now lets create an node for calculating the answer for this 

def calculate_answer(state: AgentState) -> AgentState:
    """
    Single node that performs addition or multiplication
    based on the operator passed in state.
    """

    if state["operator"] == "+":
        answer = sum(state["values"])

    elif state["operator"] == "*":
        # Multiply all elements
        answer = functools.reduce(operator.mul, state["values"], 1)

    else:
        raise ValueError("Operator must be '+' or '*'")

    state["result"] = f"Hi {state['name']} your answer is {answer}"
    return state


graph = StateGraph(AgentState)

graph.add_node("calculator",calculate_answer)
graph.set_entry_point("calculator")
graph.set_finish_point("calculator")


app = graph.compile()

# -------- EXECUTION --------
input_data = {
    "name": "jack sparrow",
    "values": [1, 2, 3, 4],
    "operator": "*",
    "result": ""
}

output = app.invoke(input_data)

print(output["result"])