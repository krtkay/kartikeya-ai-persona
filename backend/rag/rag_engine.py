from openai import OpenAI

from backend.config import OPENAI_API_KEY

from backend.rag.query_router import QueryRouter
from backend.rag.retriever import Retriever


client = OpenAI(
    api_key=OPENAI_API_KEY
)


class RAGEngine:

    def __init__(self):

        self.router = QueryRouter()

        self.retriever = Retriever()

    def answer_question(
        self,
        query
    ):

        route = self.router.route(
            query
        )

        print(
            "\nROUTER OUTPUT:",
            route
        )

        docs = self.retriever.retrieve(
            query=query,
            document_type=route.get(
                "document_type"
            ),
            repo=route.get(
                "repo"
            )
        )

        context_parts = []

        for doc in docs:

            metadata = doc["metadata"]

            context_parts.append(
                f"""
Repository:
{metadata.get('repo')}

Document Type:
{metadata.get('document_type')}

Content:
{doc['text']}
"""
            )

        context = "\n\n".join(
            context_parts
        )

        system_prompt = """
You are Kartikeya's AI representative.

Answer naturally.

Never dump README sections.

Never dump markdown.

Never dump raw commit logs.

Summarize information into clean conversational English.

If discussing projects:

- explain purpose
- explain tech stack
- explain architecture
- explain tradeoffs
- explain future improvements

If discussing commits:

summarize project evolution naturally.

Only use supplied context.

If context is insufficient,
say you don't know.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
Question:

{query}

Context:

{context}
"""
                }
            ]
        )

        return (
            response
            .choices[0]
            .message.content
        )