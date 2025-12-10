# app/cli.py
from app.rag import answer_question, format_source


def run_cli():
    print("RAG Chatbot ready... (type 'exit' to quit)\n")

    while True:
        q = input("Question: ")
        if q.lower() in ("exit", "quit"):
            break

        answer, sources = answer_question(q)
        print("\nAnswer:\n", answer)

        print("\nSources:")
        if not sources:
            print("  (No relevant documents were used)")
        else:
            seen = set()
            i = 1
            for doc in sources:
                md = doc.metadata or {}
                key = (md.get("source"), md.get("page"))
                if key in seen:
                    continue
                seen.add(key)

                friendly = format_source(doc)
                print(f"  {i}. {friendly}")
                i += 1


if __name__ == "__main__":
    run_cli()
