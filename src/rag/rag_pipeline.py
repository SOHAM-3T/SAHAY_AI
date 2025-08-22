from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
# Fix relative import
try:
    from .retriever import build_retriever
except ImportError:
    # Fallback for when running directly
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from rag.retriever import build_retriever
import os


class CareerRAGPipeline:
    def __init__(self, pdf_path: str):
        self.retriever = build_retriever(pdf_path)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        # Initialize LLM for career guidance - USE MUCH SMALLER MODEL
        self.llm = self._setup_llm()

        # Build conversation chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
        )

    def _setup_llm(self):
        # Use a MUCH smaller, faster model for career guidance
        qa_pipeline = pipeline(
            "text-generation",
            model="distilgpt2",  # Only 82MB vs 863MB - 10x smaller!
            device=-1,
            max_length=100,  # Limit response length for speed
            do_sample=True,
            temperature=0.7,
        )
        return HuggingFacePipeline(pipeline=qa_pipeline)

    def get_career_advice(self, question: str) -> dict:
        """Get personalized career advice based on resume and question"""
        try:
            result = self.chain.invoke({"question": question})  # Use .invoke() instead of deprecated __call__
            return {
                "answer": result["answer"],
                "sources": [doc.page_content for doc in result["source_documents"]],
            }
        except Exception as e:
            return {"error": str(e)}

    def analyze_skills_gap(self, target_role: str) -> dict:
        """Analyze skills gap for a specific target role"""
        question = f"What skills do I need to develop to become a {target_role}?"
        return self.get_career_advice(question)
