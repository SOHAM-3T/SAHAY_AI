import os
import sys
import logging
from typing import Dict, List, Optional
import traceback

# Fix the import path issue
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')

# Add src to Python path properly
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    # Now try to import RAG components
    from rag.rag_pipeline import CareerRAGPipeline
    from utils.pdf_parser import extract_text_from_pdf
    from utils.resume_parser import parse_resume
    RAG_AVAILABLE = True
    logging.info("RAG components imported successfully!")
except ImportError as e:
    logging.warning(f"RAG components not available: {e}")
    RAG_AVAILABLE = False
    # Print more details for debugging
    print(f"Import error details: {e}")
    print(f"Python path: {sys.path}")
    print(f"Looking for modules in: {src_path}")

class RAGService:
    """Service layer for RAG operations"""
    
    def __init__(self):
        self.rag_pipeline = None
        self.current_resume_path = None
        self.current_resume_data = None
        self._model_loaded = False  # Track if model is loaded
        logging.info(f"RAGService initialized. RAG_AVAILABLE: {RAG_AVAILABLE}")
        
    def initialize_rag(self, resume_path: str) -> bool:
        """Initialize RAG pipeline with a resume"""
        if not RAG_AVAILABLE:
            logging.warning("RAG not available, cannot initialize")
            return False
            
        try:
            logging.info(f"Initializing RAG with resume: {resume_path}")
            
            # Parse resume first
            raw_text = extract_text_from_pdf(resume_path)
            parsed_data = parse_resume(raw_text)
            
            # Initialize RAG pipeline (this will download/load the model)
            if not self._model_loaded:
                logging.info("Loading AI model for the first time...")
                self.rag_pipeline = CareerRAGPipeline(resume_path)
                self._model_loaded = True
                logging.info("AI model loaded successfully!")
            else:
                logging.info("Reusing already loaded AI model...")
                # Create new pipeline but reuse loaded model
                self.rag_pipeline = CareerRAGPipeline(resume_path)
            
            self.current_resume_path = resume_path
            self.current_resume_data = parsed_data
            
            logging.info("RAG pipeline initialized successfully!")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize RAG: {e}")
            traceback.print_exc()
            return False
    
    def get_career_advice(self, question: str) -> Dict:
        """Get AI-powered career advice using RAG"""
        if not self.rag_pipeline:
            return {"error": "RAG pipeline not initialized"}
            
        try:
            logging.info(f"Getting career advice for: {question}")
            result = self.rag_pipeline.get_career_advice(question)
            logging.info(f"RAG response: {result}")
            return result
        except Exception as e:
            logging.error(f"Error getting career advice: {e}")
            return {"error": str(e)}
    
    def analyze_skills_gap_rag(self, target_role: str) -> Dict:
        """Analyze skills gap using RAG"""
        if not self.rag_pipeline:
            return {"error": "RAG pipeline not initialized"}
            
        try:
            logging.info(f"Analyzing skills gap for role: {target_role}")
            result = self.rag_pipeline.analyze_skills_gap(target_role)
            logging.info(f"Skills gap analysis result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error analyzing skills gap: {e}")
            return {"error": str(e)}
    
    def get_resume_data(self) -> Optional[Dict]:
        """Get current resume data"""
        return self.current_resume_data
    
    def is_available(self) -> bool:
        """Check if RAG is available"""
        return RAG_AVAILABLE and self.rag_pipeline is not None

# Global RAG service instance
rag_service = RAGService() 