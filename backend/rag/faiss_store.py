import faiss
import pickle
import numpy as np
import os


class FaissStore:

    def __init__(self):

        self.dimension = 1536

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.documents = []

    def add_document(
        self,
        text,
        embedding,
        metadata
    ):

        vector = np.array(
            [embedding],
            dtype=np.float32
        )

        self.index.add(vector)

        self.documents.append(
            {
                "text": text,
                "metadata": metadata
            }
        )

    def save(self):

        faiss.write_index(
            self.index,
            "faiss.index"
        )

        with open(
            "documents.pkl",
            "wb"
        ) as f:

            pickle.dump(
                self.documents,
                f
            )

    def load(self):

        if os.path.exists(
            "faiss.index"
        ):
            self.index = faiss.read_index(
                "faiss.index"
            )

        if os.path.exists(
            "documents.pkl"
        ):
            with open(
                "documents.pkl",
                "rb"
            ) as f:

                self.documents = pickle.load(f)