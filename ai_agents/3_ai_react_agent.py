"""
Reasoning and acting agent 

here we use the tools 

Learn how to creaste the tools in langgraph 
how to create a react graph 
work with differnt types of messages type such as tool message
 test out the robustness of our graph 
"""

from typing import Annotated ,Sequence,TypedDict
from langchain_core.messages import ToolMessage, BaseMessage,SystemMessage
from langchain_ollama import ChatOllama 
from langchain_core.tools import tool # for making tools
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode 
 

# Annotated used to add the description in the field of the 
# typedict class it is just used to add the description or lets say metadata to the field 

# sequence is used to automatically handle the stat us udpates for sequences such as by adding new messagse to a chat history 

# add_message from langgraph.graphs.message is a reducer function 
# rule that controls how updates from nodes are combined with the existing state . 
# tells us how to merge new data into the current state 

# without a reducer , updates would have , replaced the existing value entirely  !