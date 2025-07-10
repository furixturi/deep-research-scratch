class Memory:
    def __init__(self):
        self.steps = []

    def add_user_input(self, prompt: str):
        self.steps.append({"role": "user", "content": prompt})

    def add_model_step(self, content: str):
        self.steps.append({"role": "model", "content": content})

    def add_step(self, type_: str, content: str):
        self.steps.append({"type": type_, "content": content})

    def format_context(self):
        return "\n".join(step["content"] for step in self.steps if "content" in step)
