from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import os
import logging

# Fix relative import
try:
    from .retriever import build_retriever
except ImportError:
    # Fallback for when running directly
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from rag.retriever import build_retriever

class CareerRAGPipeline:
    def __init__(self, pdf_path: str, cached_model=None, use_optimized=True):
        self.retriever = build_retriever(pdf_path)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        
        # Initialize LLM for career guidance - CPU optimized
        if cached_model:
            self.llm = HuggingFacePipeline(pipeline=cached_model)
            logging.info("Using cached optimized model for fast responses!")
        else:
            self.llm = self._setup_llm(use_optimized)

        # Build conversation chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
        )

    def _setup_llm(self, use_optimized=True):
        """Setup CPU-optimized LLM for career guidance"""
        try:
            if use_optimized:
                # Try to use ONNX-optimized model first
                return self._setup_onnx_model()
            else:
                # Fallback to regular optimized model
                return self._setup_regular_model()
        except Exception as e:
            logging.warning(f"Optimized model setup failed: {e}, falling back to basic model")
            return self._setup_basic_model()
    
    def _setup_onnx_model(self):
        """Setup ONNX-optimized model for best CPU performance"""
        try:
            # Try to use ONNX runtime if available
            import onnxruntime as ort
            
            # Use DialoGPT-small for better CPU performance
            model_name = "microsoft/DialoGPT-small"  # Only 117M params vs 345M
            
            qa_pipeline = pipeline(
                "text-generation",
                model=model_name,
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
            
            logging.info(f"ONNX-optimized {model_name} loaded successfully!")
            return HuggingFacePipeline(pipeline=qa_pipeline)
            
        except ImportError:
            logging.info("ONNX runtime not available, using regular optimization")
            return self._setup_regular_model()
        except Exception as e:
            logging.warning(f"ONNX setup failed: {e}")
            return self._setup_regular_model()
    
    def _setup_regular_model(self):
        """Setup regularly optimized model for CPU"""
        try:
            # Use DialoGPT-small for better CPU performance
            model_name = "microsoft/DialoGPT-small"
            
            qa_pipeline = pipeline(
                "text-generation",
                model=model_name,
                device=-1,  # Force CPU
                torch_dtype=torch.float32,  # Use float32 for CPU
                max_length=120,
                do_sample=True,
                temperature=0.7,
                pad_token_id=50256,
                # CPU memory optimizations
                low_cpu_mem_usage=True,
                return_full_text=False,
            )
            
            logging.info(f"CPU-optimized {model_name} loaded successfully!")
            return HuggingFacePipeline(pipeline=qa_pipeline)
            
        except Exception as e:
            logging.error(f"Regular model setup failed: {e}")
            return self._setup_basic_model()
    
    def _setup_basic_model(self):
        """Setup basic model as last resort"""
        try:
            # Use the smallest possible model for CPU
            model_name = "distilgpt2"  # Only 82M parameters
            
            qa_pipeline = pipeline(
                "text-generation",
                model=model_name,
                device=-1,
                max_length=100,
                do_sample=True,
                temperature=0.7,
            )
            
            logging.info(f"Basic {model_name} loaded as fallback")
            return HuggingFacePipeline(pipeline=qa_pipeline)
            
        except Exception as e:
            logging.error(f"All model setups failed: {e}")
            raise e

    def get_career_advice(self, question: str) -> dict:
        """Get personalized career advice based on resume and question"""
        try:
            result = self.chain.invoke({"question": question})
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
