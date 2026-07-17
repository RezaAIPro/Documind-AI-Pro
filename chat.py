import ollama
from memory import MemoryManager


class ChatEngine:
    def __init__(self):
        self.memory = MemoryManager()
        self.history = self.memory.load()

        if not self.history:
            self.history = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Always answer in Persian language."
                }
            ]

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

        self.memory.save(self.history)

        return answer

    def clear(self):
        self.history = []
        self.memory.clear()