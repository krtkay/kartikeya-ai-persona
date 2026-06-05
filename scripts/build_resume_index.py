import uuid

from backend.rag.ingest_resume import ResumeParser
from backend.rag.chunker import ResumeChunker
from backend.rag.embeddings import create_embedding
from backend.rag.faiss_store import FaissStore


print("Loading Resume...")

parser = ResumeParser(
    "uploads/resume.pdf"
)

sections = parser.extract_sections()

chunker = ResumeChunker()

store = FaissStore()

total_chunks = 0

for section_name, content in sections.items():

    print(
        f"\nProcessing {section_name}"
    )

    chunks = chunker.chunk_text(
        content
    )

    for chunk in chunks:

        embedding = create_embedding(
            chunk
        )

        store.add_document(
            text=chunk,
            embedding=embedding,
            metadata={
                "source": "resume",
                "section": section_name
            }
        )

        total_chunks += 1

store.save()

print(
    f"\nIndexed {total_chunks} chunks"
)