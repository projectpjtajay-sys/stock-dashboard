import os
import io
from typing import Dict, Any, List, Union
from openai import OpenAI
import config
from llama_index.core import Document

# LangChain imports
from langchain_community.document_loaders import (
    PyPDFLoader,
    PDFPlumberLoader, 
    UnstructuredPDFLoader,
    Docx2txtLoader,
    TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document as LangChainDocument
import tempfile

class EnhancedDocumentProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.storage_path = "/home/iauro/Documents/files"
        
        # Category-specific folders
        self.category_folders = {
            "engineering": "Engineer",
            "medical": "Doctor", 
            "legal": "Lawyer"
        }
        
        # Supported file types with their corresponding loaders
        self.supported_formats = {
            '.pdf': ['pypdf', 'pdfplumber', 'unstructured'],
            '.docx': ['docx'],
            '.txt': ['text'],
            '.doc': ['unstructured']
        }
        
        # Initialize text splitter with optimized settings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Ensure directories exist
        os.makedirs(self.storage_path, exist_ok=True)
        self._create_category_folders()
        
    def _create_category_folders(self):
        """Create category-specific folders if they don't exist"""
        for category, folder_name in self.category_folders.items():
            folder_path = os.path.join(self.storage_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Category folder ensured: {folder_path}")
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        return os.path.splitext(filename.lower())[1]
    
    def _is_supported_format(self, filename: str) -> bool:
        """Check if file format is supported"""
        ext = self._get_file_extension(filename)
        return ext in self.supported_formats
    
    def _load_pdf_with_fallback(self, temp_file_path: str) -> List[LangChainDocument]:
        """Load PDF using multiple loaders with fallback strategy"""
        documents = []
        
        # Try PyPDFLoader first (fastest)
        try:
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()
            if documents and any(doc.page_content.strip() for doc in documents):
                print("Successfully loaded PDF with PyPDFLoader")
                return documents
        except Exception as e:
            print(f"PyPDFLoader failed: {e}")
        
        # Try PDFPlumberLoader (better for complex layouts)
        try:
            loader = PDFPlumberLoader(temp_file_path)
            documents = loader.load()
            if documents and any(doc.page_content.strip() for doc in documents):
                print("Successfully loaded PDF with PDFPlumberLoader")
                return documents
        except Exception as e:
            print(f"PDFPlumberLoader failed: {e}")
        
        # Try UnstructuredPDFLoader (most robust)
        try:
            loader = UnstructuredPDFLoader(temp_file_path)
            documents = loader.load()
            if documents and any(doc.page_content.strip() for doc in documents):
                print("Successfully loaded PDF with UnstructuredPDFLoader")
                return documents
        except Exception as e:
            print(f"UnstructuredPDFLoader failed: {e}")
        
        return []
    
    def _load_document(self, file_content: bytes, filename: str) -> List[LangChainDocument]:
        """Load document using appropriate LangChain loader"""
        ext = self._get_file_extension(filename)
        
        # Create temporary file for LangChain loaders
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            documents = []
            
            if ext == '.pdf':
                documents = self._load_pdf_with_fallback(temp_file_path)
            
            elif ext == '.docx':
                loader = Docx2txtLoader(temp_file_path)
                documents = loader.load()
            
            elif ext == '.txt':
                loader = TextLoader(temp_file_path, encoding='utf-8')
                documents = loader.load()
            
            elif ext == '.doc':
                # Use UnstructuredLoader for .doc files
                loader = UnstructuredPDFLoader(temp_file_path)
                documents = loader.load()
            
            return documents
            
        except Exception as e:
            print(f"Error loading document with LangChain: {e}")
            return []
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def save_document_file(self, file_content: bytes, filename: str, category: str = "engineering") -> str:
        """Save document file to category-specific storage directory"""
        try:
            folder_name = self.category_folders.get(category, "Engineer")
            category_path = os.path.join(self.storage_path, folder_name)
            
            # Generate unique filename
            import time
            timestamp = int(time.time())
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{timestamp}{ext}"
            
            file_path = os.path.join(category_path, unique_filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            print(f"Document saved to: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error saving document file: {e}")
            return ""
    
    def categorize_document_content(self, text: str, filename: str) -> Dict[str, Any]:
        """Categorize document content into engineering, medical, or legal"""
        # Truncate text for classification
        sample_text = text[:2000] if len(text) > 2000 else text
        
        categorization_prompt = f"""
        Analyze the following document content and classify it into one of these categories:
        - engineering: software development, programming, technical documentation, DevOps, system design, technology
        - medical: health, medical procedures, anatomy, diseases, treatments, medical research, healthcare
        - legal: law, contracts, legal procedures, regulations, court documents, legal advice, compliance
        
        Document filename: {filename}
        Content sample: {sample_text}
        
        Return your response in JSON format with this exact structure:
        {{"category": "engineering|medical|legal"}}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": categorization_prompt}],
                max_tokens=50,
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            category = result.get("category", "engineering").strip().lower()
            
            # Validate category
            if category not in ["engineering", "medical", "legal"]:
                category = "engineering"  # default fallback
                
            return {
                "category": category,
                "filename": filename,
                "text_length": len(text),
                "sample_text": sample_text[:200]
            }
            
        except Exception as e:
            print(f"Error categorizing document: {e}")
            return {
                "category": "engineering",
                "filename": filename,
                "text_length": len(text),
                "sample_text": text[:200] if text else ""
            }
    
    def create_document_chunks(self, documents: List[LangChainDocument], metadata: Dict[str, Any]) -> List[Document]:
        """Split documents into chunks using LangChain text splitter and convert to LlamaIndex documents"""
        all_chunks = []
        
        for doc_idx, langchain_doc in enumerate(documents):
            if not langchain_doc.page_content.strip():
                continue
                
            # Split the document content
            chunks = self.text_splitter.split_text(langchain_doc.page_content)
            
            for chunk_idx, chunk_text in enumerate(chunks):
                if chunk_text.strip():
                    # Combine original metadata with new metadata
                    chunk_metadata = metadata.copy()
                    chunk_metadata.update({
                        "chunk_index": len(all_chunks),
                        "doc_page": doc_idx,
                        "total_chunks": len(chunks),
                        "page_number": langchain_doc.metadata.get("page", doc_idx)
                    })
                    
                    # Convert to LlamaIndex Document
                    llama_doc = Document(
                        text=chunk_text,
                        metadata=chunk_metadata
                    )
                    all_chunks.append(llama_doc)
        
        return all_chunks
    
    def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Complete document processing pipeline using LangChain loaders"""
        try:
            # Check if file format is supported
            if not self._is_supported_format(filename):
                return {
                    "success": False, 
                    "error": f"Unsupported file format. Supported: {list(self.supported_formats.keys())}"
                }
            
            # Load document using LangChain loaders
            documents = self._load_document(file_content, filename)
            if not documents:
                return {"success": False, "error": "Could not extract content from document"}
            
            # Combine all document text for categorization
            full_text = "\n".join([doc.page_content for doc in documents if doc.page_content.strip()])
            if not full_text.strip():
                return {"success": False, "error": "Document appears to be empty"}
            
            # Categorize content
            categorization = self.categorize_document_content(full_text, filename)
            category = categorization["category"]
            
            # Save document file
            saved_path = self.save_document_file(file_content, filename, category)
            if not saved_path:
                return {"success": False, "error": "Could not save document file"}
            
            # Create chunks using LangChain text splitter
            document_chunks = self.create_document_chunks(documents, {
                "source": filename,
                "category": category,
                "type": self._get_file_extension(filename)[1:],  # Remove the dot
                "file_path": saved_path
            })
            
            return {
                "success": True,
                "category": category,
                "filename": filename,
                "file_path": saved_path,
                "text_length": len(full_text),
                "num_chunks": len(document_chunks),
                "num_pages": len(documents),
                "documents": document_chunks,
                "sample_text": categorization["sample_text"]
            }
            
        except Exception as e:
            print(f"Error processing document: {e}")
            return {"success": False, "error": str(e)}

# Maintain backward compatibility
class PDFProcessor(EnhancedDocumentProcessor):
    """Backward compatible wrapper for the enhanced document processor"""
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Backward compatible method for PDF text extraction"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(pdf_file)
                temp_file_path = temp_file.name
            
            # Load using LangChain
            documents = self._load_pdf_with_fallback(temp_file_path)
            
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            if documents:
                return "\n".join([doc.page_content for doc in documents])
            return ""
            
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def categorize_pdf_content(self, text: str, filename: str) -> Dict[str, Any]:
        """Backward compatible method"""
        return self.categorize_document_content(text, filename)
    
    def process_pdf(self, pdf_file, filename: str) -> Dict[str, Any]:
        """Backward compatible method for PDF processing"""
        return self.process_document(pdf_file, filename) 