class Memory:
    def __init__(self):
        self.messages = []

    def add_system_prompt(self, prompt: str):
        self.messages.insert(0, {"role": "system", "content": prompt})

    def add_user_input(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})

    def add_model_step(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def add_tool_step(self, content: str):
        self.messages.append({"role": "tool", "content": content})

    def get_messages(self):
        return self.messages.copy()