from langgraph.graph import StateGraph ,END
from typing import TypedDict,List
import random

class AgentState (TypedDict): 
    player_name : str
    guesses: List[int]
    attempts : int
    lower_bound: int 
    upper_bound : int 
    hint : str
    target_number : int 


# lets make the setup node for first starting with the name

def setup_node(state : AgentState)-> AgentState:
    """basic user greeting with the player name"""
    state['player_name'] = f"welcome {state['player_name']}!"
    state['target_number']=random.randint(1,20)
    state['guesses']=[]
    state['attempts'] = 0 
    state['lower_bound']=1
    state['upper_bound']=20
    print(f"{state['player_name']} the game has begun . I'm  thinking of number between 1 and 20  ")
    return state


def guess_node(state:AgentState)-> AgentState: 
    """generate the smarter guess based on the previous hints """
    possible_guesses = [i for i in range(state["lower_bound"], state["upper_bound"] + 1) if i not in state["guesses"]]
    if possible_guesses:
        guess = random.choice(possible_guesses)
    else : 
        guess = random.randint(state['lower_bound'],state['upper_bound'])
    
    state['guesses'].append(guess)
    state['attempts']+=1
    print(f"Attempt {state['attempts']}: Guessing {guess} (Current range: {state['lower_bound']}-{state['upper_bound']})")
    return state



def hint_node(state: AgentState) -> AgentState:
    """Here we provide a hint based on the last guess and update the bounds"""
    latest_guess = state["guesses"][-1]
    target = state["target_number"]
    
    if latest_guess < target:
        state["hint"] = f"The number {latest_guess} is too low. Try higher!"
        
        state["lower_bound"] = max(state["lower_bound"], latest_guess + 1)
        print(f"Hint: {state['hint']}")
        
    elif latest_guess > target:
        state["hint"] = f"The number {latest_guess} is too high. Try lower!"
      
        state["upper_bound"] = min(state["upper_bound"], latest_guess - 1)
        print(f"Hint: {state['hint']}")
    else:
        state["hint"] = f"Correct! You found the number {target} in {state['attempts']} attempts."
        print(f"Success! {state['hint']}")
    
    return state

def should_continue(state:AgentState)->str: 
    """Determine if we should continue guessting or end the game """

    latest_guess =state['guesses'][-1]
    if latest_guess == state['target_number']:
        print(f"game over Number has been found")
        return "end"
    elif state['attempts']>= 7: 
        print(f"game over max number of attempts reached the target number was {state['target_number']}")
    else:
        print(f"continuing total {state['attempts']} of 7 has been used")
        return "continue"


# now lets create the graph 
graph = StateGraph(AgentState)


graph.add_node('setup',setup_node)
graph.add_node('guess',guess_node)
graph.add_node('hint_node',hint_node)

graph.add_edge("setup","guess")
graph.add_edge("guess","hint_node")

graph.add_conditional_edges("hint_node",should_continue,
                            {"continue":"guess","end":END})

graph.set_entry_point("setup")

app = graph.compile()
print(app.get_graph().print_ascii())
result = app.invoke({"player_name": "Student", "guesses": [], "attempts": 0, "lower_bound": 1, "upper_bound": 20})

                                    # +-----------+  
                                    # | __start__ |
                                    # +-----------+
                                    #       *
                                    #       *
                                    #       *
                                    #   +-------+
                                    #   | setup |
                                    #   +-------+
                                    #       *
                                    #       *
                                    #       *
                                    #   +-------+
                                    #   | guess |
                                    #   +-------+
                                    #       .
                                    #       .
                                    #       .
                                    # +-----------+
                                    # | hint_node |
                                    # +-----------+
                                    #       .
                                    #       .
                                    #       .
                                    #  +---------+
                                    #  | __end__ |
                                    #  +---------+
                                    # None
                                    # welcome Student! the game has begun . I'm  thinking of number between 1 and 20
                                    # Attempt 1: Guessing 2 (Current range: 1-20)
                                    # Hint: The number 2 is too low. Try higher!
                                    # continuing total 1 of 7 has been used
                                    # Attempt 2: Guessing 19 (Current range: 3-20)
                                    # Hint: The number 19 is too low. Try higher!
                                    # continuing total 2 of 7 has been used
                                    # Attempt 3: Guessing 20 (Current range: 20-20)
                                    # Success! Correct! You found the number 20 in 3 attempts.
                                    # game over Number has been found