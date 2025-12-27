# Multi-Agent Chatbot System

A sophisticated multi-agent chatbot system powered by OpenAI GPT models, designed to handle engineering, medical, and legal queries with specialized agent responses.

## Features

### Multi-Agent Architecture
- **Engineer Agent**: Handles software development, programming, technical solutions, and DevOps queries
- **Doctor Agent**: Manages medical, health, and healthcare-related questions
- **Lawyer Agent**: Addresses legal, contracts, and legal procedure inquiries

### PDF Document Processing
- **Automatic Categorization**: PDFs are automatically classified into engineering, medical, or legal categories
- **Vector Storage**: Documents are processed and stored in vector databases for semantic search
- **Local File Storage**: Uploaded PDFs are saved to `/home/iauro/Documents/files` with timestamp-based naming
- **Intelligent Search**: Advanced search algorithms with fallback mechanisms for content retrieval

### Intelligent Query Routing
- Automatic classification of user queries to appropriate specialist agents
- Context-aware responses based on uploaded PDF documentation
- Fallback responses when no relevant documentation is available

## Technical Stack

- **Backend**: FastAPI with WebSocket support
- **AI Models**: OpenAI GPT models for text generation and classification
- **Vector Database**: Qdrant DB with HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)
- **PDF Processing**: PyPDF2 for text extraction
- **Document Management**: LlamaIndex for document chunking and management
- **Safety**: Built-in guardrails for content filtering

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp env_template.txt .env
# Edit .env with your API keys
```

3. Run the application:
```bash
python main.py
```

## PDF Upload and Storage

### File Storage Location
All uploaded PDF files are automatically saved to:
```
/home/iauro/Documents/files/
```

Files are saved with timestamp-based naming to prevent conflicts:
```
original_filename_<timestamp>.pdf
```

### PDF Processing Pipeline
1. **Upload**: PDF file is received via API endpoint
2. **Save**: File is saved to local storage directory
3. **Extract**: Text content is extracted using PyPDF2
4. **Categorize**: Content is automatically classified using OpenAI
5. **Chunk**: Text is split into manageable chunks for vector storage
6. **Store**: Chunks are stored in both Qdrant DB and local fallback storage
7. **Index**: Content becomes searchable for future queries

### Supported Operations
- `/api/upload-pdf`: Upload and process PDF documents
- Automatic categorization into engineering, medical, or legal domains
- Semantic search across uploaded documents
- Category-specific content retrieval

## API Endpoints

- `GET /`: Serve frontend interface
- `POST /api/chat`: HTTP chat endpoint
- `POST /api/upload-pdf`: Upload and process PDF documents
- `WebSocket /ws/{user_id}`: Real-time chat via WebSocket
- `GET /api/health`: System health check
- `GET /api/agents`: List available agents

## Usage

1. **Upload PDFs**: Use the `/api/upload-pdf` endpoint to upload relevant documents
2. **Ask Questions**: Send queries via chat that will be automatically routed to the appropriate specialist
3. **Get Specialized Answers**: Receive responses based on your uploaded documentation with proper disclaimers

### Query Examples
- "What are the best practices for API design?" (Engineering)
- "What are the symptoms of diabetes?" (Medical)
- "How do I draft a service agreement?" (Legal)

## Safety Features

- Input safety validation
- Content filtering for responses
- Professional disclaimers for medical and legal advice
- Educational context for all specialized responses

## Graph Visualization

The multi-agent system includes built-in LangGraph visualization capabilities to understand the workflow structure.

### Available Visualization Formats

1. **ASCII Representation**: Text-based graph structure
2. **Mermaid Diagram**: Web-compatible diagram format
3. **PNG Image**: High-quality image export (requires graphviz)

### Using the Visualization

#### Command Line Tool
```bash
# Show all visualizations
python visualize_graph.py

# Show specific format
python visualize_graph.py --format mermaid
python visualize_graph.py --format ascii
python visualize_graph.py --format png
```

#### API Endpoints
- `GET /api/graph/ascii` - ASCII representation
- `GET /api/graph/mermaid` - Mermaid diagram code
- `GET /api/graph/png` - PNG image download

#### Programmatic Access
```python
from agents import MultiAgentSystem

# Initialize system
multi_agent = MultiAgentSystem()

# Generate visualizations
multi_agent.visualize_graph_ascii()      # ASCII output
multi_agent.visualize_graph_mermaid()    # Mermaid code
multi_agent.visualize_graph_png()        # PNG file
multi_agent.show_all_visualizations()   # All formats
```

### Dependencies for Full Visualization Support
```bash
pip install graphviz grandalf  # For PNG and ASCII support
```

## Configuration

Key configuration options in `config.py`:
- OpenAI API settings
- Qdrant database connection
- Server host and port
- Token limits and temperature settings

## File Storage Details

- **Storage Path**: `/home/iauro/Documents/files`
- **Naming Convention**: `{filename}_{timestamp}.pdf`
- **Automatic Directory Creation**: Directory is created if it doesn't exist
- **File Persistence**: All uploaded files are permanently stored for future reference 