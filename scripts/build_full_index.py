from backend.rag.ingest_resume import ResumeParser
from backend.rag.chunker import ResumeChunker
from backend.rag.embeddings import create_embedding
from backend.rag.faiss_store import FaissStore
from backend.rag.github_ingestor import GitHubIngestor

store = FaissStore()

chunker = ResumeChunker()

total = 0

# =====================================
# RESUME PROCESSING
# =====================================

print("\nINDEXING RESUME...\n")

parser = ResumeParser(
    "uploads/resume.pdf"
)

sections = parser.extract_sections()

for section_name, content in sections.items():

    chunks = chunker.chunk_text(
        content
    )

    print(
        f"{section_name}: {len(chunks)} chunks"
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
                "section": section_name,
                "document_type": "resume"
            }
        )

        total += 1

# =====================================
# GITHUB PROCESSING
# =====================================

print("\nINDEXING GITHUB...\n")

github = GitHubIngestor("krtkay")

repos = github.get_repositories()

print(
    f"Found {len(repos)} repositories\n"
)

for repo in repos:

    repo_name = repo["name"]

    print("\n" + "=" * 70)
    print(f"PROCESSING: {repo_name}")
    print("=" * 70)

    # ---------------------------------
    # REPO METADATA
    # ---------------------------------

    try:

        metadata_text = f"""
Repository:
{repo_name}

Description:
{repo.get('description', '')}

Language:
{repo.get('language', '')}
"""

        embedding = create_embedding(
            metadata_text
        )

        store.add_document(
            text=metadata_text,
            embedding=embedding,
            metadata={
                "source": "github",
                "repo": repo_name,
                "document_type": "repo_metadata"
            }
        )

        total += 1

        print("✓ Repo metadata indexed")

    except Exception as e:

        print(
            f"Metadata Error: {e}"
        )

    # ---------------------------------
    # README
    # ---------------------------------

    try:

        readme = github.get_readme(
            repo_name
        )

        if readme:

            chunks = chunker.chunk_text(
                readme
            )

            print(
                f"README chunks: {len(chunks)}"
            )

            for chunk in chunks:

                embedding = create_embedding(
                    chunk
                )

                store.add_document(
                    text=chunk,
                    embedding=embedding,
                    metadata={
                        "source": "github",
                        "repo": repo_name,
                        "document_type": "readme"
                    }
                )

                total += 1

        else:

            print(
                "No README found"
            )

    except Exception as e:

        print(
            f"README Error: {e}"
        )

    # ---------------------------------
    # COMMITS
    # ---------------------------------

    try:

        commits = github.get_commits(
            repo_name,
            limit=20
        )

        print(
            f"Commit count: {len(commits)}"
        )

        for commit in commits:

            try:

                message = (
                    commit["commit"]
                    ["message"]
                )

                author = (
                    commit["commit"]
                    ["author"]
                    ["name"]
                )

                date = (
                    commit["commit"]
                    ["author"]
                    ["date"]
                )

                commit_text = f"""
Repository:
{repo_name}

Author:
{author}

Date:
{date}

Commit Message:
{message}
"""

                embedding = create_embedding(
                    commit_text
                )

                store.add_document(
                    text=commit_text,
                    embedding=embedding,
                    metadata={
                        "source": "github",
                        "repo": repo_name,
                        "document_type": "commit"
                    }
                )

                total += 1

            except Exception as e:

                print(
                    f"Commit Parse Error: {e}"
                )

    except Exception as e:

        print(
            f"Commit Fetch Error: {e}"
        )

print("\n" + "=" * 70)
print("SAVING FAISS INDEX")
print("=" * 70)

store.save()

print(
    f"\nTOTAL DOCUMENTS INDEXED: {total}"
)