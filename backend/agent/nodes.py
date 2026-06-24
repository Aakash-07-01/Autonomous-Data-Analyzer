import json
from typing import Dict, Any, List
from langchain_core.messages import ToolMessage
from langchain_groq import ChatGroq
from agent.tools import run_python, generate_chart, compute_stats, set_csv_path
from agent.prompts import SYSTEM_PROMPT

tools = [run_python, generate_chart, compute_stats]

def agent_node(state: Dict[str, Any]):
    messages = state.get("messages", [])
    csv_path = state.get("csv_path")
    iteration = state.get("iteration", 0)
    
    # Initialize LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    
    # Ensure system prompt is injected once (or let graph handle it initially)
    # The graph usually starts with the system prompt in messages.
    
    # Ensure path is set for tools
    set_csv_path(csv_path)
    
    response = llm_with_tools.invoke(messages)
    
    return {
        "messages": [response],
        "iteration": iteration + 1
    }

def tool_node(state: Dict[str, Any]):
    messages = state.get("messages", [])
    last_message = messages[-1]
    
    new_charts = []
    new_thoughts = []
    new_messages = []
    
    tool_map = {tool.name: tool for tool in tools}
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # Add a thought for calling the tool
        new_thoughts.append({
            "type": "ACT",
            "text": f"Calling `{tool_name}` with arguments: {json.dumps(tool_args)}"
        })
        
        tool = tool_map.get(tool_name)
        if tool:
            try:
                result = tool.invoke(tool_args)
                result_str = str(result)
                
                if tool_name == "generate_chart" and result_str.startswith("SUCCESS:"):
                    parts = result_str.replace("SUCCESS:", "").split("|||")
                    if len(parts) >= 3:
                        new_charts.append({"base64": parts[0], "title": parts[1], "html": parts[2]})
                        result_str = f"Chart generated successfully: {parts[1]}"
                    elif len(parts) == 2:
                        new_charts.append({"base64": parts[0], "title": parts[1], "html": ""})
                        result_str = f"Chart generated successfully: {parts[1]}"
                
                # Add observation thought
                new_thoughts.append({
                    "type": "OBS",
                    "text": f"Result from `{tool_name}`:\n{result_str[:500]}{'...' if len(result_str) > 500 else ''}"
                })
                
                new_messages.append(ToolMessage(content=result_str, tool_call_id=tool_call["id"]))
            except Exception as e:
                error_msg = f"Error executing {tool_name}: {str(e)}"
                new_thoughts.append({
                    "type": "OBS",
                    "text": error_msg
                })
                new_messages.append(ToolMessage(content=error_msg, tool_call_id=tool_call["id"]))
        else:
            new_messages.append(ToolMessage(content=f"Tool {tool_name} not found", tool_call_id=tool_call["id"]))
            
    return {"messages": new_messages, "charts": new_charts, "thoughts": new_thoughts}
