import os
import pdfplumber
import docx
import re

def clean_text(text):
    """
    Cleans raw text by removing excessive whitespace and non-printable characters.
    """
    if not text:
        return ""
    
    # Replace multiple newlines/tabs/spaces with a single space
    # This normalizes the text into a continuous stream, which is often better for NLP
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-printable characters (optional, but good for safety)
    text = text.strip()
    
    return text

def parse_pdf(file_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text_content = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # extract_text() handles layout analysis fairly well
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        return None

def parse_docx(file_path):
    """
    Extracts text from a DOCX file using python-docx.
    """
    try:
        doc = docx.Document(file_path)
        # Iterate through paragraphs and join them with newlines
        full_text = [para.text for para in doc.paragraphs]
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error parsing DOCX {file_path}: {e}")
        return None

def parse_resume(file_path):
    """
    Main entry point to parse a resume. Detects file type and calls appropriate parser.
    Returns cleaned text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    
    raw_text = ""
    
    if file_extension == '.pdf':
        raw_text = parse_pdf(file_path)
    elif file_extension in ['.docx', '.doc']: 
        # Note: .doc is binary and not supported by python-docx, but we catch it here just in case users try.
        # python-docx only supports .docx
        if file_extension == '.doc':
            print("Warning: .doc format is not natively supported. Convert to .docx or .pdf.")
            return None
        raw_text = parse_docx(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None
        
    if raw_text:
        return clean_text(raw_text)
    
    return None
