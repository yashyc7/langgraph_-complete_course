from typing import TypedDict, List
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str


# ---- Node ----
def process_value(state: AgentState) -> AgentState:
    """
    Processes input values and updates result field.
    Returns new state (avoid in-place mutation).
    """
    
    total = sum(state["values"])
    
    return {
        "values": state["values"],   # preserve input
        "name": state["name"],       # preserve input
        "result": f"Hi there {state['name']}! Your sum = {total}"
    }


# ---- Graph ----
graph = StateGraph(AgentState)

graph.add_node("processor", process_value)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

print(app.get_graph().print_ascii())


                            # +-----------+  
                            # | __start__ |
                            # +-----------+
                            #       *
                            #       *
                            #       *
                            # +-----------+
                            # | processor |
                            # +-----------+
                            #       *
                            #       *
                            #       *
                            #  +---------+
                            #  | __end__ |
                            #  +---------+
                            # None