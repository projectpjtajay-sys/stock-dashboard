# LangChain Document Loaders Integration

This document describes the enhanced document processing system that integrates LangChain loaders for improved file ingestion and processing capabilities.

## Overview

The multi-agent system has been upgraded to use LangChain's powerful document loaders instead of the basic PyPDF2 implementation. This provides significant improvements in document processing capabilities, reliability, and supported file formats.

## Key Improvements

### 1. Multiple File Format Support
- **PDF**: Using PyPDFLoader, PDFPlumberLoader, and UnstructuredPDFLoader with fallback strategy
- **DOCX**: Using Docx2txtLoader for Microsoft Word documents
- **TXT**: Using TextLoader for plain text files
- **DOC**: Using UnstructuredPDFLoader for legacy Word documents

### 2. Enhanced Text Processing
- **Better Text Splitting**: LangChain's `RecursiveCharacterTextSplitter` replaces simple character-based chunking
- **Semantic Preservation**: Better handling of document structure and context
- **Configurable Parameters**: Customizable chunk size, overlap, and separators

### 3. Robust PDF Processing
- **Fallback Strategy**: Multiple PDF loaders tried in sequence for maximum compatibility
- **Better Error Handling**: Graceful degradation when one loader fails
- **Improved Text Extraction**: Better handling of complex PDF layouts

## Architecture

### Enhanced Document Processor

The new `EnhancedDocumentProcessor` class provides:

```python
class EnhancedDocumentProcessor:
    def __init__(self):
        # LangChain text splitter with optimized settings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Supported file formats with loader strategies
        self.supported_formats = {
            '.pdf': ['pypdf', 'pdfplumber', 'unstructured'],
            '.docx': ['docx'],
            '.txt': ['text'],
            '.doc': ['unstructured']
        }
```

### PDF Fallback Strategy

For PDF processing, the system tries multiple loaders in order:

1. **PyPDFLoader** - Fastest, good for simple PDFs
2. **PDFPlumberLoader** - Better for complex layouts and tables
3. **UnstructuredPDFLoader** - Most robust, handles complex documents

### Backward Compatibility

The original `PDFProcessor` class remains available as a wrapper around the enhanced processor, ensuring existing code continues to work without modifications.

## API Endpoints

### New Document Upload Endpoint

```http
POST /api/upload-document
```

**Supported File Types**: PDF, DOCX, TXT, DOC

**Response**:
```json
{
    "success": true,
    "message": "Document 'example.docx' successfully processed and categorized as 'engineering'",
    "details": {
        "filename": "example.docx",
        "file_path": "/home/iauro/Documents/files/Engineer/example_1234567890.docx",
        "category": "engineering",
        "file_type": "docx",
        "text_length": 5420,
        "num_chunks": 8,
        "num_pages": 3,
        "sample_text": "This is a sample document..."
    }
}
```

### Legacy Compatibility

The original PDF endpoint remains available:

```http
POST /api/upload-pdf
```

This endpoint now redirects to the new document upload endpoint internally.

## Dependencies

The following new dependencies have been added to `requirements.txt`:

```
# LangChain dependencies for document loaders
langchain>=0.1.0
langchain-community>=0.0.10
langchain-text-splitters>=0.0.1
unstructured>=0.10.0
pdfplumber>=0.9.0
python-docx>=0.8.11
openpyxl>=3.1.0
```

## Installation & Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test the Implementation

Run the test script to verify the enhanced processor:

```bash
python test_langchain_loader.py
```

### 3. Start the Server

```bash
python main.py
```

### 4. Upload Documents

Use the web interface or API to upload various document types:

- Open `http://localhost:8000` in your browser
- Drag and drop supported files (PDF, DOCX, TXT, DOC)
- Documents are automatically categorized and processed

## Frontend Updates

The web interface has been updated to support multiple file types:

- **File Type Validation**: Client-side validation for supported formats
- **Enhanced Upload Messages**: Shows file type, category, and processing details
- **Better Error Handling**: Clear error messages for unsupported formats

## Benefits

### 1. Improved Reliability
- Multiple fallback loaders for PDF processing
- Better error handling and recovery
- More robust text extraction

### 2. Enhanced Capability
- Support for multiple document formats
- Better text chunking and semantic preservation
- Improved metadata extraction

### 3. Better User Experience
- Support for common office document formats
- More detailed processing feedback
- Clearer error messages

### 4. Maintainability
- Cleaner, more modular code structure
- Leverages well-tested LangChain components
- Easier to extend with new file types

## Future Enhancements

The LangChain integration opens up possibilities for:

- **Additional File Types**: PowerPoint (PPTX), Excel (XLSX), CSV
- **Advanced Processing**: Table extraction, image analysis, metadata enrichment
- **Custom Loaders**: Domain-specific document processing
- **Enhanced Chunking**: Semantic-aware text splitting strategies

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed correctly
2. **PDF Processing Failures**: The fallback strategy should handle most cases, but some corrupted PDFs may fail
3. **Large File Handling**: Consider implementing file size limits for production use

### Debug Mode

To enable verbose logging for document processing, modify the logging level in the processor initialization.

## Testing

Use the provided test script to verify functionality:

```bash
# Test the enhanced processor
python test_langchain_loader.py

# Start the server and test via web interface
python main.py
```

The test script validates:
- Supported file format detection
- Text splitter configuration
- Directory structure setup
- Basic text processing capabilities 