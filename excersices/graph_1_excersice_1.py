"""
create an personalised  compliant agent using langgraph 

input : {"name":"bob"}
output : "Bob you are doing amazing job learning langgraph !" 

"""



from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict  ):
    name : str 



# lets create a node which done our tasks 


def greeting(state: AgentState)->AgentState: 
    """a simpler node which returns the greeting """

    state['name'] =  state["name"]+"you are doing amazing job learning langgraph !" 

    return state 
# now lets create the graph state 

graph = StateGraph(AgentState)


graph.add_node("greeting",greeting)

graph.set_entry_point("greeting")
graph.set_finish_point("greeting")

app = graph.compile()

print(app.get_graph(xray=True).print_ascii())


                        # (.venv) PS C:\Users\yashc\Desktop\langgraph_ complete_course> py .\graph_1_excersice_1.py
                        # +-----------+  
                        # | __start__ |  
                        # +-----------+  
                        #       *        
                        #       *        
                        #       *        
                        # +----------+   
                        # | greeting |   
                        # +----------+   
                        #       *        
                        #       *
                        #       *
                        #  +---------+
                        #  | __end__ |
                        #  +---------+
                        # None