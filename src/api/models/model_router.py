from typing import Union
import os
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

from api.config_loader import load_default_config

load_dotenv()

# Endpoints and credntials
## AOAI
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_KEY = os.getenv("AOAI_KEY")
AOAI_VERSION = os.getenv("AOAI_VERSION")
## OpenAI
OPENAI_KEY = os.getenv("OPENAI_KEY")

# load default configuration
# _default_config = load_default_config()
_default_model_config = load_default_config().get("models", {})
_supported_providers_models = _default_model_config.get("supported", {})


# Model call dispatcher
def call_model(
    messages: list,
    model_config: dict = {},
    agent_id: str = "default",
    tools: list = None,
) -> Union[str, object]:
    """
    Call the model with the provided messages and configuration.

    Args:
        messages (list): List of messages to send to the model.
        model_config (dict): Configuration dictionary for the model call.
            E.g. {"provider": "aoai", "model": "gpt-4o"}
        agent_id (str): Identifier for the agent, default is "default".
        tools (list, optional): List of tools available to the model.

    Returns:
        Union[str, object]: The response from the model. Returns str for
            regular content, or message object when tool calls are made.
    """
    model_config = _get_model_config(model_config, agent_id)
    model_provider = model_config.get("provider", "")
    model = model_config.get("model", "")

    if model_provider not in _supported_providers_models:
        raise ValueError(
            f"Model provider '{model_provider}' is not supported. "
            f"Supported providers are: {_supported_providers_models.keys()}"
        )
    if model not in _supported_providers_models.get(model_provider, []):
        raise ValueError(
            f"Model '{model}' is not supported for provider "
            f"'{model_provider}'. Supported models are: "
            f"{_supported_providers_models.get(model_provider, [])}"
        )

    if model_provider == "aoai":
        return call_aoai(messages, model, tools)
    elif model_provider == "openai":
        return call_openai(messages, model, tools)
    else:
        raise ValueError(
            f"Handler not implemented for model provider: {model_provider}"
        )


def _get_model_config(
    model_config: dict, agent_id: str = "default"
) -> dict:
    """
    Get the model configuration from default_config.yaml then override with the provided config and agent ID.

    Args:
        config (dict): Configuration dictionary.
        agent_id (str): Identifier for the agent, default is "default".

    Returns:
        dict: Model configuration dictionary
    """
    default_agent_model_config = _default_model_config.get(agent_id, {})
    model_config = {
        **_default_model_config.get("default", {}),
        **default_agent_model_config,
        **model_config,
    }
    if not model_config:
        raise ValueError(
            f"No model configuration found for agent ID: {agent_id}"
        )

    return model_config


def _is_oai_nextgen_model(model: str) -> bool:
    return model.startswith("o")


def call_aoai(
    messages: list, model: str, tools: list = None
) -> Union[str, object]:
    """
    Call the Azure OpenAI model with the provided messages.

    Args:
        messages (list): List of messages to send to the model.
        model (str): The model name to use for the call.
        tools (list, optional): List of tools available to the model.

    Returns:
        Union[str, object]: The response from the Azure OpenAI model.
            Returns str for regular content, or message object with tool calls.
    """
    client = AzureOpenAI(
        azure_endpoint=AOAI_ENDPOINT,
        api_key=AOAI_KEY,
        api_version=AOAI_VERSION,
    )

    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": 1.0,
        "top_p": 1.0,
    }

    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    if _is_oai_nextgen_model(model):
        kwargs["max_completion_tokens"] = 10000
    else:
        kwargs["max_tokens"] = 4096

    response = client.chat.completions.create(**kwargs)

    # Handle tool calls vs regular content
    message = response.choices[0].message
    if message.tool_calls:
        return message  # Return the full message with tool calls
    else:
        return message.content


def call_openai(
    messages: list, model: str, tools: list = None
) -> Union[str, object]:
    """
    Call the OpenAI model with the provided messages.

    Args:
        messages (list): List of messages to send to the model.
        model (str): The model name to use for the call.
        tools (list, optional): List of tools available to the model.

    Returns:
        Union[str, object]: The response from the OpenAI model.
            Returns str for regular content, or message object with tool calls.
    """
    client = OpenAI(api_key=OPENAI_KEY)

    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": 1.0,
        "top_p": 1.0,
    }

    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    if _is_oai_nextgen_model(model):
        kwargs["max_completion_tokens"] = 10000
    else:
        kwargs["max_tokens"] = 4096

    response = client.chat.completions.create(**kwargs)

    # Handle tool calls vs regular content
    message = response.choices[0].message
    if message.tool_calls:
        return message  # Return the full message with tool calls
    else:
        return message.content


##############
#### STUB ####
##############
# def call_model(prompt: str, config: dict) -> str:
#     return (
#         "Thought: I am a stub thought. Still, I should use a tool to answer.\n"
#         "Action: search\n"
#         "Action Input: NVIDIA revenue 2024"
#     )
