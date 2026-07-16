import ollama

class ChatEngine:
    def __init__(self):
        self.history = []

    def chat(self, message, model):
        self.history.append({
            "role": "user",
            "content": message
        })

        response = ollama.chat(
            model=model,
            messages=self.history
        )

        answer = response["message"]["content"]

        self.history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    def clear(self):
        self.history = []