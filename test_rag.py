from backend.rag.rag_engine import RAGEngine

print("=" * 60)
print("KARTIKEYA AI PERSONA TEST")
print("=" * 60)

rag = RAGEngine()

while True:

    query = input("\nYou: ")

    if query.lower() in [
        "exit",
        "quit",
        "q"
    ]:
        break

    try:

        response = rag.answer_question(
            query
        )

        print(
            f"\nAI: {response}\n"
        )

    except Exception as e:

        print(
            f"\nERROR: {e}\n"
        )