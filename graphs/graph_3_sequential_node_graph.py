from langgraph.graph import StateGraph
from typing import TypedDict


class AgentState(TypedDict):
    name : str 
    age : int
    final : str 


# now create the node functions 

def first_node(state : AgentState)->AgentState: 
    state['final']=  f"{state['name']}"

    return state 
    

def second_node(state:AgentState)->AgentState: 
    state['final']= state['final']+f'You are{state['age']} years old '

    return state

graph = StateGraph(AgentState)
 


graph.add_node("first_node",first_node)
graph.add_node("second_node",second_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node","second_node")

graph.set_finish_point("second_node")



app = graph.compile()

print(app.get_graph().print_ascii())

                    #  +-----------+   
                    #  | __start__ |   
                    #  +-----------+   
                    #         *        
                    #         *        
                    #         *
                    # +------------+
                    # | first_node |
                    # +------------+
                    #         *
                    #         *
                    #         *
                    # +-------------+
                    # | second_node |
                    # +-------------+
                    #         *
                    #         *
                    #         *
                    #   +---------+
                    #   | __end__ |
                    #   +---------+

answer = app.invoke({"name":"charlie","age":29})

print(answer)