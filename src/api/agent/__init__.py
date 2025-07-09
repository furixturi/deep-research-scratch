"""Routing to single agent or multi-agent according to config"""

from .single_agent import run_single_agent
from .multi_agents.planner_agent import run_planner_agent


async def run_agent(prompt: str, config: dict) -> str:
    """
    Run the agent based on the provided configuration.

    Args:
        prompt (str): The input prompt for the agent.
        config (dict): Configuration dictionary to determine which agent to run.

    Returns:
        str: The response from the agent.
    """
    agent_type = config.get(
        "agent_type", "single_agent"
    ).lower()  # Default to single_agent if not specified
    if agent_type == "single_agent":
        return await run_single_agent(prompt, config)
    elif agent_type == "planner_agent":
        return await run_planner_agent(prompt, config)
    else:
        raise ValueError(
            f"Unknown agent type: {agent_type}. Supported types are 'single_agent' and 'planner_agent'."
        )
