#lets first import libraries 

from langgraph.graph import StateGraph 

from typing import List,TypedDict 


class AgentState(TypedDict):
    name: str
    age : int
    skills : List[str]
    final_result : str

# we have three nodes here 

def first_node(state:AgentState)->AgentState:
    """ personalises the name field with greeting

    Args:
        state (AgentState): state of the application

    Returns:
        AgentState: return the updated state 
    """

    state['final_result'] = f"{state['name']} welcome to the system!"
    return state 

def second_node(state:AgentState)->AgentState:
    """Describes the user's Age 

    Args:
        state (AgentState): state of the current application

    Returns:
        AgentState: returns the updated state with age 
    """ 
    state['final_result'] = state['final_result']+ f"you are {state['age']} years old ! "

    return state 

def third_node(state:AgentState)->AgentState : 
    """List the user skills in the formatted string

    Args:
        state (AgentState): state of the current system 

    Returns:
        AgentState:  returns the final answer with updated state 

    """

    state['final_result'] = state['final_result']+ f"You have skills in {','.join(state['skills'])}"
    return state 


graph = StateGraph(AgentState)

graph.add_node("first_node",first_node)
graph.add_node("second_node",second_node)
graph.add_node("third_node",third_node)

graph.set_entry_point("first_node")
 
graph.add_edge("first_node","second_node")
graph.add_edge("second_node","third_node")
graph.set_finish_point("third_node")

app = graph.compile()



print(app.get_graph().print_ascii())


                        # | __start__ |
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
                        # +------------+
                        # | third_node |
                        # +------------+
                        #         *
                        #         *
                        #         *
                        #   +---------+
                        #   | __end__ |
                        #   +---------+
                        # None



result = app.invoke({"name": "Linda", "age": 31, "skills":["Python", "Machine Learning", "LangGraph"]})

print(result)

# {'name': 'Linda', 'age': 31, 'skills': ['Python', 'Machine Learning', 'LangGraph'], 'final_result': "Linda welcome to the system!you are 31 years old ! You have skills in ['Python', 'Machine Learning', 'LangGraph']"}