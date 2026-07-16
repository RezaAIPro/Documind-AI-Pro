import re


class SearchEngine:

    def __init__(self):
        pass

    def search(self, text, query, chunk_size=1200):

        if not text:
            return ""

        chunks = []

        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])

        query_words = re.findall(r"\w+", query.lower())

        best_chunk = ""
        best_score = -1

        for chunk in chunks:

            score = 0

            chunk_lower = chunk.lower()

            for word in query_words:
                score += chunk_lower.count(word)

            if score > best_score:
                best_score = score
                best_chunk = chunk

        return best_chunk