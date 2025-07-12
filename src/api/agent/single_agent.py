import json

from api.models.model_router import call_model
from api.agent.memory import Memory
from api.tools import (
    get_available_tools,
    get_tools_openai_format,
    execute_tool,
)

tools = get_available_tools()

SYSTEM_PROMPT = (
    "You are a helpful research assistant following the ReAct (Reasoning and Acting) framework. "
    "You have access to tools that can help you answer questions. "
    "When you need to search for information, use the search tool. "
    "When you need to execute code, use the code tool. "
    "Always use the appropriate tools to provide accurate and helpful responses. "
    "Do not just describe what you would do - actually use the tools available to you. "
    "\n\n"
    "IMPORTANT: Always structure your responses in the following format:\n"
    "Thought: [Your reasoning about what you need to do]\n"
    "Action: [The tool you want to use]\n"
    "Action Input: [The input/parameters for the tool]\n"
    "\n"
    "After receiving tool results, continue with:\n"
    "Thought: [Your analysis of the results]\n"
    "Action: [Next tool to use, or 'Final Answer' if done]\n"
    "Action Input: [Tool parameters, or your final answer]\n"
    "\n"
    "When you have enough information to answer the user's question, provide:\n"
    "Thought: [Your reasoning about the complete answer]\n"
    "Final Answer: [Your complete answer to the user's question]\n"
    "\n"
    "Always think step by step and use the tools to gather information before providing your final answer."
)


def print_tool_call_debug(
    tool_name: str,
    tool_args: str,
    tool_call_id: str,
    tool_result: str,
):
    """Print debug output for tool call steps"""
    print(f"> Tool name: {tool_name}")
    print(f"> Tool arg: {tool_args}")
    print(f"> Tool call ID: {tool_call_id}")
    print(f"< Tool result: {tool_result}")


def print_text_step_debug(step_count: int, content: str):
    """Print debug output for text response steps"""
    print(content)


def print_react_debug(
    step_count: int,
    thought: str = None,
    action: str = None,
    action_input: str = None,
    tool_result: str = None,
):
    """Print ReAct-style debug output"""
    if thought:
        print(f"- {thought}")
    if action:
        print(f"- {action}")
    if action_input:
        print(f"- {action_input}")
    if tool_result:
        print(f"- Tool Result: {tool_result}")


def extract_react_components(response_content: str) -> dict:
    """Extract Thought, Action, and Action Input from model response"""
    if not response_content:
        return {"thought": None, "action": None, "action_input": None}

    lines = response_content.split("\n")
    thought = None
    action = None
    action_input = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract components based on ReAct format
        if line.startswith("Thought:"):
            thought = line  # Keep the full "Thought: ..." line
        elif line.startswith("Action:"):
            action = line  # Keep the full "Action: ..." line
        elif line.startswith("Action Input:"):
            action_input = (
                line  # Keep the full "Action Input: ..." line
            )
        elif line.startswith("Final Answer:"):
            # If we find Final Answer, that's the thought for this step
            thought = line  # Keep the full "Final Answer: ..." line
            action = None  # No action for final answer
            action_input = None  # No action input for final answer
            break

    # If no explicit thought found, extract from first meaningful line
    if not thought:
        for line in lines:
            line = line.strip()
            if line and not line.startswith(
                ("Action:", "Action Input:", "Final Answer:")
            ):
                thought = line
                break

    return {
        "thought": thought,
        "action": action,
        "action_input": action_input,
    }


# ReAct Agent Loop
async def run_single_agent(prompt: str, config: dict) -> str:
    memory = Memory()
    memory.add_system_prompt(SYSTEM_PROMPT)
    memory.add_user_input(prompt)

    step_count = 0
    max_steps = config.get("max_steps", 5)
    tools_openai_format = get_tools_openai_format()

    # Debug: Print available tools and schemas when agent starts
    print("\n" + "=" * 60)
    print("AGENT STARTING - AVAILABLE TOOLS:")
    for tool in tools_openai_format:
        tool_name = tool["function"]["name"]
        tool_desc = tool["function"]["description"]
        print(f"  • {tool_name}: {tool_desc}")
    print("=" * 60)

    print(f"\nTOOL SCHEMAS:")
    print(json.dumps(tools_openai_format, indent=2))

    # Log initial user question (not as a model thought)
    print("\n" + "=" * 60)
    print(f"\nUSER QUESTION: {prompt}")
    print("=" * 60)

    while step_count < max_steps:
        step_count += 1
        print(f"\n=== STEP {step_count} ===")

        # Call model with tools
        response = call_model(
            memory.get_messages(),
            config,
            agent_id="single_agent",
            tools=tools_openai_format,
        )

        # Check if response is a message object (with tool calls) or string
        print(f"\n*** Raw response ***\n {response}")

        if hasattr(response, "tool_calls") and response.tool_calls:

            # Handle tool calls - extract components from response content
            response_content = (
                response.content if hasattr(response, "content") else ""
            )

            # Log the full response for debugging
            print(f"\n### Response has Tool Calls ###")
            print(f"Tool calls: {len(response.tool_calls)}")

            react_components = extract_react_components(
                response_content
            )

            # Log the model's ReAct components first
            if (
                react_components["thought"]
                or react_components["action"]
                or react_components["action_input"]
            ):
                print(f"\n### Response also has TEXT ###")
                print_react_debug(
                    step_count,
                    thought=react_components["thought"],
                    action=react_components["action"],
                    action_input=react_components["action_input"],
                )

            # Add model response to memory
            memory.add_model_step(response)

            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                tool_args_json = tool_call.function.arguments
                tool_call_id = tool_call.id

                try:
                    parsed_args = json.loads(tool_args_json)
                except Exception as e:
                    print(f"Error parsing tool args: {e}")
                    parsed_args = {"input": tool_args_json}

                # Execute the tool using the tools module
                tool_result = execute_tool(tool_name, parsed_args)

                # Print tool call debug in the new format
                tool_result_text = (
                    tool_result[:500] + "..."
                    if len(str(tool_result)) > 500
                    else str(tool_result)
                )
                print_tool_call_debug(
                    tool_name,
                    tool_args_json,
                    tool_call_id,
                    tool_result_text,
                )

                # Add tool result to memory
                memory.add_tool_step(tool_call_id, tool_result)

        elif isinstance(response, str):
            # Handle regular text response
            print(f"\n### Response is TEXT only ###")

            print_text_step_debug(step_count, response)

            memory.add_model_step(response)

            # Check for final answer
            if "Final Answer" in response:
                final_answer = response.split("Final Answer:", 1)[
                    -1
                ].strip()
                return final_answer

        else:
            # Handle message object without tool calls
            content = (
                response.content
                if hasattr(response, "content")
                else str(response)
            )

            print(f"\n### Response is neither TOOL CALL nor TEXT ###")
            print(f"Response content: {content}")
            print(f"Response type: {type(response)}")

            memory.add_model_step(content)

            # Check for final answer
            if "Final Answer" in content:
                final_answer = content.split("Final Answer:", 1)[
                    -1
                ].strip()
                return final_answer

    final_result = (
        f"[Stopped after {max_steps} steps - no final answer]"
    )
    print(f"\n{final_result}")
    return final_result


##############
#### STUB ####
##############
# async def run_single_agent(prompt: str, config: dict) -> str:
#     """
#     Run a single agent with the provided prompt and configuration.

#     Args:
#         prompt (str): The input prompt for the agent.
#         config (dict): Configuration dictionary for the agent.

#     Returns:
#         str: The response from the agent.
#     """
#     # Here you would implement the logic to run a single agent
#     # For demonstration purposes, we will just return a mock response
#     return f"[Single Agent /stub] You said: {prompt} with config: {config}"
