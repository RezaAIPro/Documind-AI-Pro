import re


class MemoryExtractor:

    def extract(self, text):

        memory = {}

        # Name
        match = re.search(
            r"اسم من\s+(.+?)(?:\s+است|\s+ه)?$",
            text.strip()
        )

        if match:
            memory["name"] = match.group(1).strip()

        # Age
        match = re.search(
            r"(\d+)\s*سال",
            text
        )

        if match:
            memory["age"] = int(match.group(1))

        # City
        match = re.search(
            r"من اهل\s+(.+)$",
            text
        )

        if match:
            memory["city"] = match.group(1).strip()

        # Job
        match = re.search(
            r"شغل من\s+(.+)$",
            text
        )

        if match:
            memory["job"] = match.group(1).strip()

        # Goal
        match = re.search(
            r"هدفم\s+(.+)$",
            text
        )

        if match:
            memory["goals"] = match.group(1).strip()

        # Likes
        match = re.search(
            r"من\s+(.+)\s+را دوست دارم",
            text
        )

        if match:
            memory["preferences"] = match.group(1).strip()

        return memory