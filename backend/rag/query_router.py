import json

from openai import OpenAI

from backend.config import OPENAI_API_KEY
from backend.rag.repo_registry import RepoRegistry


client = OpenAI(
    api_key=OPENAI_API_KEY
)


class QueryRouter:

    def __init__(self):

        self.registry = RepoRegistry()

    def route(self,query):

        query_lower = query.lower()

        resume_keywords = [

            "skill",
            "skills",
            "experience",
            "education",
            "internship",
            "internships",
            "resume",
            "background",
            "career",
            "qualification",
            "qualifications",
            "technologies",
            "tech stack",
            "strengths"

        ]

        for keyword in resume_keywords:

            if keyword in query_lower:

                return {
                    "repo": None,
                    "document_type": "resume"
                }

        repos = (
            self.registry
            .get_repo_names()
        )

        prompt = f"""
    You are a query routing engine.

    Available repositories:

    {repos}

    Determine:

    1. Which repository is being referenced.
    2. Which document type is needed.

    Document types:

    - resume
    - readme
    - commit

    Rules:

    - Questions about projects, architecture, tech stack, implementation → readme
    - Questions about updates, changes, commit history → commit
    - Questions about education, experience, skills, internships → resume

    Return ONLY valid JSON.

    Example:

    {{
        "repo": "vulgarVeto",
        "document_type": "commit"
    }}

    Question:

    {query}
    """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        try:

            return json.loads(
                response.choices[0]
                .message.content
            )

        except Exception:

            return {
                "repo": None,
                "document_type": None
            }