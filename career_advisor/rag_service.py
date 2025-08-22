import os
import sys
import logging
from typing import Dict, List, Optional
import traceback
import pickle
import hashlib

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
    """Service layer for RAG operations with CPU-optimized model caching"""
    
    def __init__(self):
        self.rag_pipeline = None
        self.current_resume_path = None
        self.current_resume_data = None
        self._model_cache = {}  # Cache for different resume hashes
        self._global_model = None  # Global model instance
        self._model_info = {}  # Track model performance info
        logging.info(f"RAGService initialized. RAG_AVAILABLE: {RAG_AVAILABLE}")
        
    def _get_resume_hash(self, resume_path: str) -> str:
        """Generate hash for resume content to enable caching"""
        try:
            with open(resume_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return resume_path
    
    def _load_global_model(self):
        """Load the CPU-optimized AI model once and keep it in memory"""
        if self._global_model is None:
            try:
                logging.info("Loading CPU-optimized DialoGPT-small model into memory...")
                # Import here to avoid circular imports
                from transformers import pipeline
                import torch
                
                # Load the CPU-optimized model
                self._global_model = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-small",  # Only 117M params vs 345M
                    device=-1,  # Force CPU
                    torch_dtype=torch.float32,  # Use float32 for CPU compatibility
                    max_length=120,  # Reasonable response length
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=50256,
                    # CPU optimizations
                    low_cpu_mem_usage=True,
                    return_full_text=False,
                )
                
                # Store model info
                self._model_info = {
                    "model_name": "microsoft/DialoGPT-small",
                    "parameters": "117M",
                    "optimization": "CPU-optimized",
                    "memory_usage": "Low",
                    "response_time": "Fast"
                }
                
                logging.info("CPU-optimized DialoGPT-small model loaded successfully!")
                logging.info(f"Model info: {self._model_info}")
                
            except Exception as e:
                logging.error(f"Failed to load global model: {e}")
                self._global_model = None
                # Try fallback to even smaller model
                try:
                    logging.info("Trying fallback to DistilGPT2...")
                    self._global_model = pipeline(
                        "text-generation",
                        model="distilgpt2",  # Only 82M parameters
                        device=-1,
                        max_length=100,
                        do_sample=True,
                        temperature=0.7,
                    )
                    self._model_info = {
                        "model_name": "distilgpt2",
                        "parameters": "82M",
                        "optimization": "Ultra-lightweight",
                        "memory_usage": "Very Low",
                        "response_time": "Very Fast"
                    }
                    logging.info("Fallback DistilGPT2 model loaded successfully!")
                except Exception as fallback_e:
                    logging.error(f"Fallback model also failed: {fallback_e}")
                    self._global_model = None
    
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
            
            # Generate resume hash for caching
            resume_hash = self._get_resume_hash(resume_path)
            
            # Check if we have cached pipeline for this resume
            if resume_hash in self._model_cache:
                logging.info("Using cached RAG pipeline for this resume")
                self.rag_pipeline = self._model_cache[resume_hash]
            else:
                # Load global model if not already loaded
                self._load_global_model()
                
                if self._global_model is None:
                    logging.error("Global model failed to load")
                    return False
                
                # Create new RAG pipeline with cached model
                logging.info("Creating new RAG pipeline with cached model...")
                self.rag_pipeline = CareerRAGPipeline(resume_path, cached_model=self._global_model)
                
                # Cache this pipeline
                self._model_cache[resume_hash] = self.rag_pipeline
                logging.info("RAG pipeline cached for future use")
            
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
    
    def get_cache_info(self) -> Dict:
        """Get information about model caching and performance"""
        return {
            "global_model_loaded": self._global_model is not None,
            "cached_pipelines": len(self._model_cache),
            "rag_available": self.is_available(),
            "model_info": self._model_info,
            "performance_tips": [
                "Using CPU-optimized model for better performance",
                "Model cached in memory for instant responses",
                "Low memory usage for stable operation"
            ]
        }

# Global RAG service instance
rag_service = RAGService() 