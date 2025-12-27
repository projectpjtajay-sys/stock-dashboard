from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
import json
import os
import uvicorn
import config
from agents import MultiAgentSystem
from vector_store import VectorStoreManager
from guardrails import SafetyGuardrails
from pdf_processor import PDFProcessor

app = FastAPI(title="Multi-Agent Chatbot", version="1.0.0")

# Initialize components
multi_agent = MultiAgentSystem()
vector_store = VectorStoreManager()
guardrails = SafetyGuardrails()
pdf_processor = PDFProcessor()

# Initialize knowledge base
try:
    vector_store.add_knowledge_base()
    print("Knowledge base initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize knowledge base: {e}")

class ChatMessage(BaseModel):
    message: str
    user_id: str = "default"

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User {user_id} disconnected")

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))

manager = ConnectionManager()

@app.get("/")
async def get_frontend():
    """Serve the frontend HTML file"""
    return FileResponse("frontend.html")

@app.post("/api/chat")
async def chat_endpoint(chat_message: ChatMessage):
    """HTTP endpoint for chat (fallback if WebSocket not available)"""
    try:
        response = await process_message(chat_message.message, chat_message.user_id)
        return {"success": True, "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process document (PDF, DOCX, TXT, DOC)"""
    try:
        # Get supported file extensions
        supported_extensions = ['.pdf', '.docx', '.txt', '.doc']
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        # Validate file type
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Supported formats: {', '.join(supported_extensions)}"
            )
        
        # Read file content
        content = await file.read()
        
        # Process document using enhanced processor
        result = pdf_processor.process_document(content, file.filename)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Add to vector store
        success = vector_store.add_pdf_documents(result["documents"], result["category"])
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to store document in vector database")
        
        return {
            "success": True,
            "message": f"Document '{file.filename}' successfully processed and categorized as '{result['category']}'",
            "details": {
                "filename": result["filename"],
                "file_path": result.get("file_path", ""),
                "category": result["category"],
                "file_type": result.get("type", file_extension[1:]),
                "text_length": result["text_length"],
                "num_chunks": result["num_chunks"],
                "num_pages": result.get("num_pages", 1),
                "sample_text": result["sample_text"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

# Keep the old endpoint for backward compatibility
@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF document (legacy endpoint)"""
    # Redirect to the new document upload endpoint
    return await upload_document(file)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, user_id)
    
    # Send welcome message
    welcome_msg = {
        "type": "system",
        "message": "Connected to Multi-Agent Chatbot! Ask questions about engineering, medical topics, or legal matters.",
        "timestamp": str(int(__import__("time").time()))
    }
    await manager.send_personal_message(welcome_msg, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if user_message.strip():
                # Process the message
                response = await process_message(user_message, user_id)
                
                # Send response back to client
                await manager.send_personal_message(response, user_id)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        error_msg = {
            "type": "error",
            "message": f"An error occurred: {str(e)}",
            "timestamp": str(int(__import__("time").time()))
        }
        await manager.send_personal_message(error_msg, user_id)
        manager.disconnect(user_id)

async def process_message(message: str, user_id: str) -> Dict[str, Any]:
    """Process user message through the multi-agent system"""
    try:
        # Safety check
        safety_check = guardrails.check_input_safety(message)
        if not safety_check["safe"]:
            return {
                "type": "agent_response",
                "message": safety_check["message"],
                "agent": "safety",
                "specialist_field": "safety",
                "timestamp": str(int(__import__("time").time()))
            }
        
        # Process through multi-agent system (no pre-context needed, agents will search PDFs directly)
        result = multi_agent.process_query(message, vector_store)
        
        # Apply safety filters
        filtered_response = guardrails.filter_response(
            result["response"], 
            result["selected_agent"]
        )
        
        return {
            "type": "agent_response",
            "message": filtered_response,
            "agent": result["selected_agent"],
            "specialist_field": result["specialist_field"],
            "original_query": message,
            "timestamp": str(int(__import__("time").time()))
        }
        
    except Exception as e:
        print(f"Error processing message: {e}")
        return {
            "type": "error",
            "message": "I apologize, but I encountered an error processing your request. Please try again.",
            "timestamp": str(int(__import__("time").time()))
        }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agents": ["engineer", "doctor", "lawyer"]}

@app.get("/api/agents")
async def get_agents():
    """Get available agents"""
    return {
        "agents": [
            {
                "name": "engineer",
                "description": "Software engineering and technical expertise",
                "specialties": ["programming", "system design", "devops", "security"]
            },
            {
                "name": "doctor",
                "description": "Medical knowledge and health advice",
                "specialties": ["symptoms", "preventive care", "first aid", "mental health"]
            },
            {
                "name": "lawyer",
                "description": "Legal guidance and advice",
                "specialties": ["contract law", "employment law", "criminal law", "business law"]
            }
        ]
    }

@app.get("/api/graph/ascii")
async def get_graph_ascii():
    """Get ASCII representation of the multi-agent graph"""
    try:
        # Capture the ASCII output
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        multi_agent.visualize_graph_ascii()
        
        sys.stdout = old_stdout
        ascii_output = buffer.getvalue()
        
        return {"success": True, "ascii_graph": ascii_output}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/graph/mermaid")
async def get_graph_mermaid():
    """Get Mermaid diagram representation of the multi-agent graph"""
    try:
        mermaid_graph = multi_agent.visualize_graph_mermaid()
        if mermaid_graph:
            return {"success": True, "mermaid_graph": mermaid_graph}
        else:
            return {"success": False, "error": "Could not generate Mermaid graph"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/graph/png")
async def get_graph_png():
    """Generate and return PNG visualization of the multi-agent graph"""
    try:
        import os
        png_filename = "multiagent_graph.png"
        multi_agent.visualize_graph_png(png_filename)
        
        if os.path.exists(png_filename):
            return FileResponse(
                png_filename, 
                media_type="image/png",
                filename="multiagent_graph.png"
            )
        else:
            return {"success": False, "error": "PNG file was not generated"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("Starting Multi-Agent Chatbot Server...")
    print(f"Available at: http://{config.HOST}:{config.PORT}")
    uvicorn.run(app, host=config.HOST, port=config.PORT) 