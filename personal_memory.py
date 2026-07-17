import json
import os


class PersonalMemory:
    def __init__(self):
        self.file = "user_memory.json"

        if not os.path.exists(self.file):
            self.save({
                "name": "",
                "age": "",
                "city": "",
                "country": "",
                "job": "",
                "language": "",
                "preferences": [],
                "skills": [],
                "goals": []
            })

    def load(self):
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update(self, key, value):
        data = self.load()

        if key in ["preferences", "skills", "goals"]:
            if value not in data[key]:
                data[key].append(value)
        else:
            data[key] = value

        self.save(data)

    def build_prompt(self):
        data = self.load()

        prompt = "User Information:\n"

        for key, value in data.items():
            if value:
                prompt += f"{key}: {value}\n"

        return prompt