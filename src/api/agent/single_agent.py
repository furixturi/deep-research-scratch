from models.model_router import call_model
from agent.memory import Memory

SYSTEM_PROMPT = (
    "You are a helpful research assistant."
    "You think step by step and use tools when needed. \n"
    "Respond using this format:\n"
    "Thought: <your reasoning>\n"
    "Action: <tool name or Final Answer>\n"
    "Action Input: <input to tool or answer>\n"
)

TOOLS = ["search", "code", "Final Answer"]

async def run_single_agent(prompt: str, config: dict) -> str:
    memory = Memory()
    memory.add_user_input(prompt)

    while True:
        context = memory.format_context()
        model_input = SYSTEM_PROMPT + context
        response = call_model(model_input, config)

        memory.add_model_step(response)

        # Parse model output
        lines = response.strip().splitlines()
        thought = next((l for l in lines if l.startswith("Thought:")), "")
        action = next((l for l in lines if l.startswith("Action:")), "")
        action_input = next((l for l in lines if l.startswith("Action Input:")), "")

        memory.add_step("thought", thought)
        memory.add_step("action", action)
        memory.add_step("action_input", action_input)

        if action == "Action: Final Answer":
            return action_input.replace("Action Input:", "").strip()
        
        # TODO: tool call
        observation = f"[Tool '{action}' not implemented yet]"
        memory.add_step("observation", observation)






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
