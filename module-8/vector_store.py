from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from llama_index.core import Document
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import uuid
import config
import os
import json
import PyPDF2

class VectorStoreManager:
    def __init__(self):
        self.client = None
        # Separate collections for different categories
        self.collections = {
            "engineering": "engineer_knowledge",
            "medical": "doctor_knowledge", 
            "legal": "lawyer_knowledge"
        }
        # Category-specific folders (same as in PDFProcessor)
        self.category_folders = {
            "engineering": "Engineer",
            "medical": "Doctor", 
            "legal": "Lawyer"
        }
        self.use_qdrant = False
        self.local_documents = []  # Fallback storage
        self.embed_model = None
        self.storage_path = "/home/iauro/Documents/files"
        self.metadata_file = os.path.join(self.storage_path, "documents_metadata.json")
        print("VectorStoreManager initialized with separate collections for Engineer, Doctor, and Lawyer")
        
        # Ensure category folders exist
        self._create_category_folders()
        
        try:
            # Initialize HuggingFace embeddings
            self.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
            print("HuggingFace embeddings initialized")
        except Exception as e:
            print(f"HuggingFace embeddings failed, using fallback: {e}")
        
        try:
            self.client = QdrantClient(
                url=config.QDRANT_URL,
                api_key=config.QDRANT_API_KEY if config.QDRANT_API_KEY else None
            )
            # Test connection
            self.client.get_collections()
            self.use_qdrant = True
            print("Qdrant DB connected successfully")
        except Exception as e:
            print(f"Qdrant DB not available, using local storage: {e}")
            self.use_qdrant = False
        
        # Load existing documents from storage
        self._load_existing_documents()
    
    def _create_category_folders(self):
        """Create category-specific folders if they don't exist"""
        os.makedirs(self.storage_path, exist_ok=True)
        for category, folder_name in self.category_folders.items():
            folder_path = os.path.join(self.storage_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Category folder ensured: {folder_path}")
    
    def _load_existing_documents(self):
        """Load existing PDF documents from storage into memory"""
        try:
            print("_load_existing_documents: Loading documents from metadata file")
            if os.path.exists(self.metadata_file):
                print("Loading existing documents from metadata...")
                with open(self.metadata_file, 'r') as f:
                    stored_docs = json.load(f)
                
                for doc_info in stored_docs:
                    file_path = doc_info.get('file_path', '')
                    if os.path.exists(file_path):
                        # Reload the PDF content
                        with open(file_path, 'rb') as pdf_file:
                            content = pdf_file.read()
                            text = self._extract_text_from_bytes(content)
                            if text:
                                # Recreate document chunks
                                chunks = self._create_document_chunks(text, doc_info['metadata'])
                                self.local_documents.extend(chunks)
                                print(f"Reloaded: {doc_info['filename']} ({len(chunks)} chunks)")
                
                print(f"Loaded {len(self.local_documents)} document chunks from storage")
            else:
                print("No existing document metadata found")
        except Exception as e:
            print(f"Error loading existing documents: {e}")
    
    def _extract_text_from_bytes(self, pdf_content: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            import io
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
            print("_extract_text_from_bytes: Extracted text from PDF bytes")
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def _create_document_chunks(self, text: str, metadata: dict) -> list:
        """Create document chunks from text"""
        chunk_size = 1000
        overlap = 200
        chunks = []
        text_length = len(text)
        
        for i in range(0, text_length, chunk_size - overlap):
            chunk_text = text[i:i + chunk_size]
            if chunk_text.strip():
                doc_metadata = metadata.copy()
                doc_metadata.update({
                    "chunk_index": len(chunks),
                    "total_chunks": (text_length // (chunk_size - overlap)) + 1
                })
                
                chunks.append(Document(
                    text=chunk_text,
                    metadata=doc_metadata
                ))
        return chunks
    
    def _save_metadata(self):
        """Save document metadata for persistence"""
        try:
            print("_save_metadata: Saving document metadata")
            # Extract unique documents (by source filename)
            unique_docs = {}
            for doc in self.local_documents:
                source = doc.metadata.get('source', 'unknown')
                if source not in unique_docs:
                    unique_docs[source] = {
                        'filename': source,
                        'metadata': {
                            'source': doc.metadata.get('source'),
                            'category': doc.metadata.get('category'),
                            'type': doc.metadata.get('type'),
                            'file_path': doc.metadata.get('file_path')
                        },
                        'file_path': doc.metadata.get('file_path', '')
                    }
            
            # Save to metadata file
            with open(self.metadata_file, 'w') as f:
                json.dump(list(unique_docs.values()), f, indent=2)
            print(f"Saved metadata for {len(unique_docs)} documents")
        except Exception as e:
            print(f"Error saving metadata: {e}")
        
    def _get_user_collection_name(self, user_id: str = "default", category: str = "engineering") -> str:
        """Generate category-specific collection name for user"""
        collection_base = self.collections.get(category, "engineer_knowledge")
        return f"user_{user_id}_{collection_base}"
    
    def _ensure_collection_exists(self, collection_name: str):
        """Ensure collection exists in Qdrant"""
        if not self.use_qdrant:
            return True
        print(f"_ensure_collection_exists: Checking/creating collection {collection_name}")
            
        try:
            if not self.client.collection_exists(collection_name):
                print(f"Creating Qdrant collection '{collection_name}'...")
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # all-MiniLM-L6-v2 has 384 dimensions
                )
                print(f"Collection '{collection_name}' created")
            return True
        except Exception as e:
            print(f"Error creating collection: {e}")
            return False
    
    def create_index(self, documents=None):
        """Legacy method - not used in new approach"""
        # This method is no longer used with the HuggingFace approach
        # Keeping for compatibility but not implementing
        return None
    
    def add_knowledge_base(self):
        """Legacy method - knowledge now comes only from uploaded PDFs"""
        # No longer adding default knowledge base
        # All knowledge must come from uploaded PDFs
        print("Knowledge base will be built from uploaded PDFs only")
        print("add_knowledge_base called")
        return True
    
    def add_pdf_documents(self, documents, category: str, user_id: str = "default"):
        """Add PDF documents to the vector store with category using your approach"""
        try:
            print(f"add_pdf_documents: Adding {len(documents)} documents to category {category} collection")
            # Always store locally as fallback
            for doc in documents:
                doc.metadata["category"] = category
                doc.metadata["source_type"] = "pdf"
                doc.metadata["user_id"] = user_id
            self.local_documents.extend(documents)
            
            # Save metadata for persistence
            self._save_metadata()
            
            # Try to store in Qdrant if available
            if self.use_qdrant and self.embed_model:
                # Get category-specific collection name
                collection_name = self._get_user_collection_name(user_id, category)
                
                # Ensure collection exists
                if not self._ensure_collection_exists(collection_name):
                    print(f"Qdrant storage failed for {category} collection, using local storage only")
                    return True
                
                # Generate embeddings
                print(f"Generating embeddings for {len(documents)} chunks in {category} collection...")
                texts = [doc.text for doc in documents]
                vectors = [self.embed_model.get_text_embedding(text) for text in texts]
                
                # Create payloads with metadata
                payloads = []
                for i, doc in enumerate(documents):
                    payload = {
                        "text": doc.text,
                        "category": category,
                        "source": doc.metadata.get("source", "unknown"),
                        "source_type": "pdf"
                    }
                    payloads.append(payload)
                
                # Upload to Qdrant
                print(f"Uploading vectors to {category} collection ({collection_name})...")
                points = []
                for i, (vector, payload) in enumerate(zip(vectors, payloads)):
                    points.append(PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload=payload
                    ))
                
                self.client.upsert(
                    collection_name=collection_name,
                    points=points
                )
                
                print(f"Added {len(documents)} PDF chunks to {category} collection in Qdrant")
            else:
                print(f"Stored {len(documents)} chunks locally ({category} category)")
                
            print(f"Total documents in memory: {len(self.local_documents)}")
            return True
            
        except Exception as e:
            print(f"Error adding PDF documents to {category} collection: {e}")
            # Documents are already stored locally as fallback
            print(f"Using local storage fallback for {len(documents)} chunks")
            return True
    
    def search_knowledge(self, query: str, agent_type: str = None, top_k: int = 3):
        """Legacy method - now redirects to PDF search with proper category mapping"""
        # Map agent types to category names for compatibility
        category_mapping = {
            "engineer": "engineering",
            "doctor": "medical", 
            "lawyer": "legal",
            "engineering": "engineering",
            "medical": "medical",
            "legal": "legal"
        }
        category = category_mapping.get(agent_type, "engineering") if agent_type else "engineering"
        return self.search_pdf_knowledge(query, category, "default", top_k)
    
    def search_pdf_knowledge(self, query: str, category: str = None, user_id: str = "default", top_k: int = 3):
        """Search specifically in PDF documents with optional category filter using your approach"""
        try:
            print(f"search_pdf_knowledge: Searching for '{query}' in category '{category}' for user '{user_id}'")
            if self.use_qdrant and self.embed_model and category:
                # Get category-specific collection name
                collection_name = self._get_user_collection_name(user_id, category)
                
                # Check if collection exists
                if not self.client.collection_exists(collection_name):
                    print(f"No {category} collection found for user {user_id}, using local search")
                    return self._local_search(query, category, top_k)
                
                # Generate query embedding
                query_vector = self.embed_model.get_text_embedding(query)
                
                # Search in the category-specific collection
                results = self.client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=top_k
                )
                
                if results:
                    context = " ".join([hit.payload["text"] for hit in results])
                    print(f"Retrieved {len(results)} results from {category} collection in Qdrant")
                    return context
                else:
                    print(f"No results found in {category} collection, trying local search")
                    return self._local_search(query, category, top_k)
            else:
                # Fallback: Simple text search in local documents
                print(f"Using local search for category: {category}")
                return self._local_search(query, category, top_k)
                
        except Exception as e:
            print(f"Error searching {category} collection: {e}")
            return self._local_search(query, category, top_k)
    
    def _local_search(self, query: str, category: str = None, top_k: int = 3):
        """Fallback search in locally stored documents"""
        print(f"_local_search: Searching locally for '{query}' in category '{category}'")
        if not self.local_documents:
            return "No PDF documents uploaded yet."
        
        # Filter by category if specified
        relevant_docs = []
        for doc in self.local_documents:
            if category is None or doc.metadata.get("category") == category:
                # More lenient text matching
                query_lower = query.lower()
                text_lower = doc.text.lower()
                
                # Remove common stop words but be more lenient
                common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
                query_words = [word for word in query_lower.split() if word not in common_words and len(word) > 1]
                
                if not query_words:  # If no significant words, use original query
                    query_words = query_lower.split()
                
                # Count meaningful matches - much more lenient
                matches = 0
                partial_matches = 0
                
                for word in query_words:
                    if word in text_lower:
                        matches += 1
                    else:
                        # Check for partial matches (substring matching)
                        for text_word in text_lower.split():
                            if word in text_word or text_word in word:
                                if len(word) > 2 and len(text_word) > 2:  # Avoid very short matches
                                    partial_matches += 0.5
                                    break
                
                total_score = matches + partial_matches
                match_ratio = total_score / len(query_words) if query_words else 0
                
                # Much lower threshold - require at least 10% relevance OR at least one exact match
                if match_ratio >= 0.1 or matches >= 1:
                    relevant_docs.append((doc, total_score))
        
        if not relevant_docs:
            # If still no matches, be even more lenient - check for any word presence
            for doc in self.local_documents:
                if category is None or doc.metadata.get("category") == category:
                    text_lower = doc.text.lower()
                    query_words = query.lower().split()
                    
                    # Find any word matches at all
                    any_match = any(word in text_lower for word in query_words if len(word) > 2)
                    if any_match:
                        relevant_docs.append((doc, 0.1))  # Low score but included
        
        if not relevant_docs:
            category_text = f" {category}" if category else ""
            return f"No relevant content found in{category_text} documents."
        
        # Sort by relevance and take top results
        relevant_docs.sort(key=lambda x: x[1], reverse=True)
        top_docs = relevant_docs[:top_k]
        
        # Combine content
        result_text = ""
        for doc, score in top_docs:
            source_name = doc.metadata.get('source', 'document')
            # Include more content from each document
            text_preview = doc.text[:500] if len(doc.text) > 500 else doc.text
            result_text += f"From {source_name}: {text_preview}\n\n"
        
        return result_text.strip() 