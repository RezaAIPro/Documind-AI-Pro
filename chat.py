import ollama

from memory import MemoryManager
from personal_memory import PersonalMemory
from memory_extractor import MemoryExtractor


class ChatEngine:

    def __init__(self):

        self.memory = MemoryManager()
        self.personal_memory = PersonalMemory()
        self.extractor = MemoryExtractor()

        self.history = self.memory.load()

        if not self.history:

            self.history = []

    def chat(self, message, model, language):

        # --------------------------
        # Save important user info
        # --------------------------

        extracted = self.extractor.extract(message)

        for key, value in extracted.items():

            self.personal_memory.update(key, value)

        # --------------------------
        # Build system prompt
        # --------------------------

        personal_info = self.personal_memory.build_prompt()

        if language == "فارسی":

            system_prompt = {
                "role": "system",
                "content": f"""
تو یک دستیار هوش مصنوعی حرفه‌ای هستی.

همیشه فارسی پاسخ بده مگر اینکه کاربر زبان دیگری بخواهد.

اطلاعاتی که از کاربر می‌دانی:

{personal_info}

اگر کاربر درباره اطلاعات شخصی خودش سؤال کرد
از اطلاعات بالا استفاده کن.
"""
            }

        else:

            system_prompt = {
                "role": "system",
                "content": f"""
You are a professional AI assistant.

Always answer in English.

Known information about the user:

{personal_info}

Use this information whenever it is useful.
"""
            }

        messages = [system_prompt] + self.history

        messages.append({
            "role": "user",
            "content": message
        })

        response = ollama.chat(
            model=model,
            messages=messages
        )

        answer = response["message"]["content"]

        self.history.append({
            "role": "user",
            "content": message
        })

        self.history.append({
            "role": "assistant",
            "content": answer
        })

        self.memory.save(self.history)

        return answer

    def clear(self):

        self.history = []

        self.memory.clear()