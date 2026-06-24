import os
from typing import TypedDict, Annotated, Sequence, List, Dict, Any
import operator
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from agent.nodes import agent_node, tool_node
from agent.prompts import SYSTEM_PROMPT

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    csv_path: str
    charts: Annotated[List[Dict[str, str]], operator.add]
    findings: str
    thoughts: Annotated[List[Dict[str, str]], operator.add]
    iteration: int

def should_continue(state: AgentState):
    messages = state["messages"]
    iteration = state["iteration"]
    
    max_iterations = int(os.environ.get("MAX_AGENT_ITERATIONS", 12))
    
    last_message = messages[-1]
    
    if iteration >= max_iterations:
        return "end"
    
    if not last_message.tool_calls:
        return "end"
        
    return "continue"

def end_node(state: AgentState):
    # Extract final text as findings
    messages = state["messages"]
    last_message = messages[-1]
    
    return {"findings": last_message.content}

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("end", end_node)
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": "end"
        }
    )
    
    workflow.add_edge("tools", "agent")
    workflow.add_edge("end", END)
    
    return workflow.compile()
