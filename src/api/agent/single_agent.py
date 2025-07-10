from api.models.model_router import call_model
from api.agent.memory import Memory
from api.tools import get_available_tools, get_tool_handler

## temporary import for test
from api.tools import search

tools = get_available_tools()
SYSTEM_PROMPT = (
    "You are a helpful research assistant. You think step by step and use tools when needed. \n"
    "Available tools:\n"
    + "\n".join(f"- {tool}: {description}" for tool, description in tools.items()) + "\n"
    "Respond using this format:\n"
    "Thought: <your reasoning>\n"
    "Action: <tool name or Final Answer>\n"
    "Action Input: <input to tool or answer>\n"
)

# ReAct Agent Loop
async def run_single_agent(prompt: str, config: dict) -> str:
    memory = Memory()
    memory.add_system_prompt(SYSTEM_PROMPT)
    memory.add_user_input(prompt)

    step_count = 0
    max_steps = config.get("max_steps", 3)

    while step_count < max_steps:
        step_count += 1

        response = call_model(memory.get_messages(), config)
        memory.add_model_step(response)

        # Parse model output
        lines = response.strip().splitlines()
        thought = next((l for l in lines if l.startswith("Thought:")), "")
        action = next((l for l in lines if l.startswith("Action:")), "")
        action_input = next((l for l in lines if l.startswith("Action Input:")), "")

        # Debug print
        print(f" --- Step {step_count} ---\n Thought: {thought}\n Action: {action}\n Action Input: {action_input}")

        if not action:
            return "[Error: Model did not return an Action.]"
        
        if action == "Action: Final Answer":
            return action_input.replace("Action Input:", "").strip()
        
        # Dummy tool simulation
        tool_name = action.replace("Action:", "").strip()
        tool_input = action_input.replace("Action Input:", "").strip()

        # Debug print
        print(f"> Calling tool '{tool_name}' with input: {tool_input}")

        tool_handler = get_tool_handler(tool_name)
        observation = tool_handler(tool_input)
        memory.add_tool_step(observation)

        # Debug print
        print(f"< Tool '{tool_name}' returned: {observation}\n")
    
    return f"[Stopped after {max_steps} steps - no final answer]"






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
