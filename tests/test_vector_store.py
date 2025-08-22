from src.utils.pdf_parser import extract_text_from_pdf
from src.utils.resume_parser import parse_resume
from src.rag.vector_store import create_vector_store


def main():
    pdf_path = "data/Resume.pdf"
    raw_text = extract_text_from_pdf(pdf_path)
    parsed = parse_resume(raw_text)

    # Create chunks per section
    chunks = [
        "Education:\n" + "\n".join(parsed["education"]),
        "Skills:\n" + ", ".join(parsed["skills"]),
        "Projects:\n" + "\n".join(parsed["projects"]),
        "Experience:\n" + "\n".join(parsed["experience"]),
    ]

    store = create_vector_store(chunks)

    query = "What should I learn to become a backend developer?"
    results = store.similarity_search(query, k=2)

    print("🔍 Retrieved Chunks:")
    for doc in results:
        print("-", doc.page_content[:200], "...\n")


if __name__ == "__main__":
    main()
