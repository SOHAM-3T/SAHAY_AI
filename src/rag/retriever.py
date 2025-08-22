from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from src.rag.vector_store import create_vector_store
from src.utils.pdf_parser import extract_text_from_pdf
from src.utils.resume_parser import parse_resume
import os
from transformers import pipeline

def build_retriever(pdf_path: str):
    # Parse resume
    raw_text = extract_text_from_pdf(pdf_path)
    parsed = parse_resume(raw_text)

    # Create chunks
    chunks = [
        "Education:\n" + "\n".join(parsed["education"]),
        "Skills:\n" + ", ".join(parsed["skills"]),
        "Projects:\n" + "\n".join(parsed["projects"]),
        "Experience:\n" + "\n".join(parsed["experience"]),
    ]

    # Build FAISS store
    store = create_vector_store(chunks)
    return store.as_retriever(search_kwargs={"k": 2})

from dotenv import load_dotenv
load_dotenv()

print(os.getenv("HUGGINGFACEHUB_API_TOKEN"))

def build_qa_chain(retriever):
    qa_pipeline = pipeline(
        "question-answering",
        model="distilbert-base-uncased-distilled-squad",
        device=-1  # CPU
    )

    # Custom QA chain: for each retrieved doc, pass to QA pipeline
    def qa_chain(inputs):
        question = inputs["query"]
        docs = retriever.get_relevant_documents(question)
        answers = []
        for doc in docs:
            answer = qa_pipeline(question=question, context=doc.page_content)["answer"]
            answers.append({"answer": answer, "source": doc.page_content})
        return {
            "result": answers[0]["answer"] if answers else "No answer found.",
            "source_documents": docs
        }

    return qa_chain