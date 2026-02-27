from typing import TypedDict
from langgraph.graph import StateGraph,START,END

class AgentState(TypedDict):
    number_1 : int 
    operation : str 
    number_2 : int 
    final_answer : int

def adder (state:AgentState)->AgentState:
    """ This node adds the two numbers

    Args:
        state (AgentState): current state of the application

    Returns:
        AgentState: returns the updated state of the application 

        
    """

    state['final_answer'] = state['number_1']+state['number_2']

    return state

def subtractor (state:AgentState)->AgentState:
    """ This node subtracts the two numbers

    Args:
        state (AgentState): current state of the application

    Returns:
        AgentState: returns the updated state of the application 

        
    """

    state['final_answer'] = state['number_1'] - state['number_2']

    return state


def multiplier (state:AgentState)->AgentState:
    """ This node product the two numbers

    Args:
        state (AgentState): current state of the application

    Returns:
        AgentState: returns the updated state of the application 

        
    """

    state['final_answer'] = state['number_1']*state['number_2']

    return state


def decide_next_node(state:AgentState)->AgentState: # router for deciding 
    """this node will select thenext node of the graph 


    Args:
        state (AgentState): current state of the application

    Returns:
        AgentState: decide and return which node to be executed next
    """
    if state['operation'] == "+":
        return "addition_operation" # edge name in future
    elif state['operation']== "-":
        return "substraction_operation"
    elif state['operation']== "*":
        return "multiplication_operation"


graph = StateGraph(AgentState)

graph.add_node("addition_node",adder)
graph.add_node("substraction_node",subtractor)
graph.add_node("multiplicator_node",multiplier)

graph.add_node("router",lambda state: state) # passthrough : your input state will be your output state 

graph.add_edge(START,"router")

graph.add_conditional_edges(
    "router",decide_next_node,
    {
        "addition_operation":"addition_node",
        "substraction_operation":"substraction_node",
        "multiplication_operation":"multiplicator_node"

    }
)

graph.add_edge(["addition_node","substraction_node","multiplicator_node"],END)


app = graph.compile()



                #                                 | __start__ |

                #                                 +-----------+

                #                                        *

                #                                        *

                #                                        *

                #                                   +--------+

                #                                 ..| router |...

                #                            .....  +--------+   .....

                #                       .....            .            .....     

                #                  .....                .                  .....
                #               ...                     .
                # ...
                # +---------------+          +--------------------+          +-------------------+
                # | addition_node |          | multiplicator_node |          | substraction_node |
                # +---------------+*****     +--------------------+        **+-------------------+
                #                       *****           *             *****     

                #                            *****       *       *****

                #                                 ***    *    ***

                #                                   +---------+
                #                                   | __end__ |
                #                                   +---------+


initial_state_1 = AgentState(number_1=1,number_2=3,operation='+')

print(app.invoke(initial_state_1))

# {'number_1': 1, 'operation': '+', 'number_2': 3, 'final_answer': 4}