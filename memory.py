import json
import os


class MemoryManager:
    def __init__(self):
        self.file = "chat_history.json"

    def load(self):
        if not os.path.exists(self.file):
            return []

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save(self, history):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def clear(self):
        if os.path.exists(self.file):
            os.remove(self.file)