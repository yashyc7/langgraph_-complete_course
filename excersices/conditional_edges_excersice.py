from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number_1: int
    number_2: int
    number_3: int
    number_4: int
    operation_1: str
    operation_2: str
    final_number_1: int
    final_number_2: int


# ---------------- ROUTERS ----------------

def router_1(state: AgentState):
    if state["operation_1"] == "+":
        return "add_node_1_edge"
    elif state["operation_1"] == "-":
        return "substract_node_1_edge"


def router_2(state: AgentState):
    if state["operation_2"] == "+":
        return "add_node_2_edge"
    elif state["operation_2"] == "-":
        return "substract_node_2_edge"


# ---------------- OPERATION NODES ----------------

def add_node_1(state: AgentState) -> AgentState:
    state["final_number_1"] = state["number_1"] + state["number_2"]
    return state


def substract_node_1(state: AgentState) -> AgentState:
    state["final_number_1"] = state["number_1"] - state["number_2"]
    return state


def add_node_2(state: AgentState) -> AgentState:
    state["final_number_2"] = state["number_3"] + state["number_4"]
    return state


def substract_node_2(state: AgentState) -> AgentState:
    state["final_number_2"] = state["number_3"] - state["number_4"]
    return state


# ---------------- GRAPH BUILD ----------------

graph = StateGraph(AgentState)

# Add nodes
graph.add_node("add_node_1", add_node_1)
graph.add_node("substract_node_1", substract_node_1)
graph.add_node("add_node_2", add_node_2)
graph.add_node("substract_node_2", substract_node_2)

# Routers (pass-through nodes)
graph.add_node("router_1", lambda state: state)
graph.add_node("router_2", lambda state: state)

# Start
graph.add_edge(START, "router_1")

# First conditional branch
graph.add_conditional_edges(
    "router_1",
    router_1,
    {
        "add_node_1_edge": "add_node_1",
        "substract_node_1_edge": "substract_node_1",
    },
)

# Merge into router_2
graph.add_edge(["add_node_1", "substract_node_1"], "router_2")

# Second conditional branch
graph.add_conditional_edges(
    "router_2",
    router_2,
    {
        "add_node_2_edge": "add_node_2",
        "substract_node_2_edge": "substract_node_2",
    },
)

# End
graph.add_edge(["add_node_2", "substract_node_2"], END)

app = graph.compile()

print(app.get_graph().print_ascii())

                            #               +-----------+
                            #               | __start__ |
                            #               +-----------+
                            #                      *
                            #                      *
                            #                      *
                            #                +----------+
                            #                | router_1 |
                            #                +----------+
                            #              ...           ...
                            #            ..                 ..
                            #          ..                     ..
                            # +------------+           +------------------+
                            # | add_node_1 |           | substract_node_1 |
                            # +------------+           +------------------+
                            #              ***           ***
                            #                 **       **
                            #                   **   **
                            #                +----------+
                            #                | router_2 |
                            #                +----------+
                            #              ...           ...
                            #            ..                 ..
                            #          ..                     ..
                            # +------------+           +------------------+
                            # | add_node_2 |           | substract_node_2 |
                            # +------------+           +------------------+
                            #              ***           ***
                            #                 **       **
                            #                   **   **
                            #                 +---------+
                            #                 | __end__ |
                            #                 +---------+
                            # None