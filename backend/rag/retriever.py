import numpy as np

from backend.rag.faiss_store import FaissStore
from backend.rag.embeddings import create_embedding


class Retriever:

    def __init__(self):

        self.store = FaissStore()
        self.store.load()

    def retrieve(
        self,
        query,
        k=15,
        document_type=None,
        repo=None
    ):

        query_embedding = create_embedding(
            query
        )

        query_vector = np.array(
            [query_embedding],
            dtype=np.float32
        )

        distances, indices = (
            self.store.index.search(
                query_vector,
                len(self.store.documents)
            )
        )

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            doc = self.store.documents[idx]

            metadata = doc["metadata"]

            if (
                document_type
                and metadata.get(
                    "document_type"
                )
                != document_type
            ):
                continue

            if repo:

                stored_repo = (
                    metadata
                    .get("repo", "")
                    .lower()
                )

                requested_repo = (
                    repo.lower()
                )

                if (
                    requested_repo
                    not in stored_repo
                ):
                    continue

            results.append(doc)

            if len(results) >= k:
                break

        return results