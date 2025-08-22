from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
import os

# Fix relative imports
try:
    from .vector_store import create_vector_store
    from ..utils.pdf_parser import extract_text_from_pdf
    from ..utils.resume_parser import parse_resume
except ImportError:
    # Fallback for when running directly
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from rag.vector_store import create_vector_store
    from utils.pdf_parser import extract_text_from_pdf
    from utils.resume_parser import parse_resume

def build_retriever(pdf_path: str):
    """Build a retriever from a PDF file"""
    try:
        # Extract text from PDF
        raw_text = extract_text_from_pdf(pdf_path)
        
        # Parse resume for structured data
        resume_data = parse_resume(raw_text)
        
        # Create text chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Combine all text data
        all_text = raw_text + "\n\n" + "\n".join(resume_data.get("skills", []))
        if resume_data.get("projects"):
            all_text += "\n\n" + "\n".join(resume_data["projects"])
        if resume_data.get("education"):
            all_text += "\n\n" + "\n".join(resume_data["education"])
        if resume_data.get("experience"):
            all_text += "\n\n" + "\n".join(resume_data["experience"])
        
        chunks = text_splitter.split_text(all_text)
        
        # Create vector store
        vector_store = create_vector_store(chunks)
        
        # Build retriever
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        return retriever
        
    except Exception as e:
        print(f"Error building retriever: {e}")
        # Return a simple fallback retriever
        return None

def build_qa_chain(retriever):
    """Build a question-answering chain"""
    try:
        # Use a lightweight model for QA
        qa_pipeline = pipeline(
            "text-generation",
            model="distilgpt2",  # Smaller, faster model
            device=-1,
        )
        
        llm = HuggingFacePipeline(pipeline=qa_pipeline)
        
        # Build QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        
        return qa_chain
        
    except Exception as e:
        print(f"Error building QA chain: {e}")
        return None
