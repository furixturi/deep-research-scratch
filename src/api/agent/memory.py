class Memory:
    def __init__(self):
        self.messages = []

    def add_system_prompt(self, prompt: str):
        self.messages.insert(0, {"role": "system", "content": prompt})

    def add_user_input(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})

    def add_model_step(self, content):
        """Add a model response to memory.
        
        Args:
            content: Can be a string or a message object with tool calls
        """
        if isinstance(content, str):
            # Regular text response
            self.messages.append({"role": "assistant", "content": content})
        elif hasattr(content, 'tool_calls') and content.tool_calls:
            # Message object with tool calls
            message_dict = {
                "role": "assistant",
                "content": content.content,
                "tool_calls": []
            }
            for tool_call in content.tool_calls:
                message_dict["tool_calls"].append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })
            self.messages.append(message_dict)
        else:
            # Fallback for other message objects
            content_str = getattr(content, 'content', str(content))
            self.messages.append({"role": "assistant", "content": content_str})

    def add_tool_step(self, tool_call_id: str, content: str):
        self.messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content,
            }
        )

    def get_messages(self):
        return self.messages.copy()
