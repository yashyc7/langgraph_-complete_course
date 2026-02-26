from typing import Dict,TypedDict
from langgraph.graph import StateGraph # framework that helps you design and manage the flow of the tasks in your application using graph . 


# we would now create an agent state , a shared data structure 
# that keeps track of the information as your application runs 

class AgentState(TypedDict):
    message : str


# defining the node  / function that do some work 

def greeting_node(state:AgentState )->AgentState: 
    """
    a simple node that adds a greeting messsage to the 
    state
    """ 

    state['message']= "hey"+state["message"] + "how is your day going ? "

    return state 

## now building a graph 

graph = StateGraph(AgentState)

# lets first add start node 




graph.add_node("greeter",greeting_node)

# compiler must know first what greeter actually is before then we can use it in the entry point and the finish point 

graph.set_entry_point("greeter")

graph.set_finish_point("greeter")


app = graph.compile() # compile the graph 



print(app.get_graph().print_ascii())

                                                # +-----------+  
                                                # | __start__ |
                                                # +-----------+
                                                #       *
                                                #       *
                                                #       *
                                                #  +---------+
                                                #  | greeter |
                                                #  +---------+
                                                #       *
                                                #       *
                                                #       *
                                                #  +---------+
                                                #  | __end__ |
                                                #  +---------+
                                                # None




