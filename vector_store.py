import faiss
import numpy as np


class VectorStore:

    def __init__(self):

        self.index = None
        self.texts = []

    def build(self, embeddings, texts):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            embeddings.astype(np.float32)
        )

        self.texts = texts

    def search(self, query_embedding, k=3):

        distances, indices = self.index.search(
            query_embedding.astype(np.float32),
            k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.texts):
                results.append(
                    self.texts[idx]
                )

        return results