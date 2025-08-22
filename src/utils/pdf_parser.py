import fitz  # PyMuPDF
import re
from typing import List, Dict, Tuple
import logging


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF with enhanced capabilities.
    Returns clean, structured text with better formatting preservation.
    """
    text = ""
    try:
        # Open PDF with PyMuPDF
        doc = fitz.open(file_path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Get text with better formatting
            page_text = page.get_text("text")
            
            # Clean up the text
            cleaned_text = clean_pdf_text(page_text)
            
            text += cleaned_text + "\n"
        
        doc.close()
        
        logging.info(f"Successfully extracted text from PDF: {file_path}")
        return text.strip()
        
    except Exception as e:
        logging.error(f"Error reading PDF {file_path}: {e}")
        return ""


def clean_pdf_text(text: str) -> str:
    """
    Clean and normalize PDF text for better parsing.
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common PDF extraction issues
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camelCase
    text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)  # Add space after punctuation
    
    # Remove page numbers and headers/footers
    text = re.sub(r'\b\d+\s*$', '', text, flags=re.MULTILINE)  # Page numbers at end of lines
    
    # Clean up bullet points and lists
    text = re.sub(r'[•·▪▫◦‣⁃]\s*', '• ', text)  # Standardize bullet points
    text = re.sub(r'^\s*[-*+]\s*', '• ', text, flags=re.MULTILINE)  # Convert dashes to bullets
    
    return text.strip()


def extract_text_with_layout(file_path: str) -> Dict[str, any]:
    """
    Extract text with layout information for better section detection.
    Returns both text and layout data.
    """
    try:
        doc = fitz.open(file_path)
        layout_data = {
            'text': '',
            'sections': [],
            'font_sizes': [],
            'positions': []
        }
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Get text blocks with position and font info
            blocks = page.get_text("dict")
            
            for block in blocks.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                layout_data['text'] += text + " "
                                layout_data['sections'].append({
                                    'text': text,
                                    'font_size': span["size"],
                                    'font_name': span["font"],
                                    'bbox': span["bbox"],
                                    'page': page_num
                                })
                                layout_data['font_sizes'].append(span["size"])
                                layout_data['positions'].append(span["bbox"])
            
            layout_data['text'] += "\n"
        
        doc.close()
        return layout_data
        
    except Exception as e:
        logging.error(f"Error extracting layout from PDF {file_path}: {e}")
        return {'text': '', 'sections': [], 'font_sizes': [], 'positions': []}


def extract_text_by_sections(file_path: str) -> Dict[str, str]:
    """
    Extract text organized by sections using font size and position analysis.
    """
    layout_data = extract_text_with_layout(file_path)
    
    if not layout_data['sections']:
        return {'full_text': layout_data['text']}
    
    # Analyze font sizes to identify headers
    font_sizes = layout_data['font_sizes']
    if font_sizes:
        avg_font_size = sum(font_sizes) / len(font_sizes)
        header_threshold = avg_font_size * 1.2  # Headers are typically larger
    else:
        header_threshold = 14
    
    sections = {}
    current_section = "general"
    current_text = []
    
    for section in layout_data['sections']:
        text = section['text']
        font_size = section['font_size']
        
        # Check if this is a header
        if font_size > header_threshold and len(text.split()) <= 4:
            # Save previous section
            if current_text:
                sections[current_section] = " ".join(current_text)
            
            # Start new section
            current_section = text.lower().replace(" ", "_")
            current_text = []
        else:
            current_text.append(text)
    
    # Save last section
    if current_text:
        sections[current_section] = " ".join(current_text)
    
    # Add full text
    sections['full_text'] = layout_data['text']
    
    return sections


def get_pdf_metadata(file_path: str) -> Dict[str, str]:
    """
    Extract PDF metadata for additional context.
    """
    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata
        doc.close()
        
        return {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'pages': len(doc)
        }
    except Exception as e:
        logging.error(f"Error extracting PDF metadata: {e}")
        return {}


if __name__ == "__main__":
    # Test the new parser
    pdf_path = "data/Resume.pdf"
    print("Testing PyMuPDF parser...")
    
    # Basic text extraction
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted text length: {len(text)} characters")
    print("First 500 characters:")
    print(text[:500])
    
    # Section-based extraction
    sections = extract_text_by_sections(pdf_path)
    print(f"\nFound sections: {list(sections.keys())}")
    
    # Metadata
    metadata = get_pdf_metadata(pdf_path)
    print(f"\nPDF Metadata: {metadata}")
