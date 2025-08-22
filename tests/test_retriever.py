from src.rag.retriever import build_retriever, build_qa_chain


def main():
    retriever = build_retriever("data/Resume.pdf")
    qa_chain = build_qa_chain(retriever)

    query = "What languages does Soham know?"
    result = qa_chain({"query": query})

    print("Answer:", result["result"])
    print("\nSources:")
    for doc in result["source_documents"]:
        print("-", doc.page_content[:200], "...\n")


if __name__ == "__main__":
    main()
