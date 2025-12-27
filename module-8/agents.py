from typing import TypedDict, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
from openai import OpenAI
import config
import os
from IPython.display import Image, display

class AgentState(TypedDict):
    messages: list
    user_query: str
    selected_agent: str
    agent_response: str
    specialist_field: str
    vector_store: Any

class MultiAgentSystem:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.graph = self.create_graph()
        
    def classify_query(self, state: AgentState) -> AgentState:
        """Classify the user query to determine which agent should handle it"""
        query = state["user_query"]
        
        classification_prompt = f"""
        Classify the following query into one of these categories:
        - engineering: software development, programming, technical solutions, coding
        - medical: health, symptoms, medical advice, diseases, treatments
        - legal: law, legal advice, contracts, rights, legal procedures
        
        Query: {query}
        
        Return your response in JSON format with this exact structure:
        {{"category": "engineering|medical|legal"}}
        """
        
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": classification_prompt}],
            max_tokens=50,
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        try:
            import json
            result = json.loads(response.choices[0].message.content)
            classification = result.get("category", "engineering").lower()
        except:
            classification = "engineering"  # fallback
        
        if "engineer" in classification or "technical" in classification:
            selected_agent = "engineer"
            specialist_field = "engineering"
        elif "medical" in classification or "health" in classification:
            selected_agent = "doctor"
            specialist_field = "medical"
        elif "legal" in classification or "law" in classification:
            selected_agent = "lawyer"
            specialist_field = "legal"
        else:
            selected_agent = "engineer"  # default
            specialist_field = "engineering"
            
        state["selected_agent"] = selected_agent
        state["specialist_field"] = specialist_field
        print(f"Classifying query: {query}")
        return state
    
    def engineer_agent(self, state: AgentState) -> AgentState:
        """Handle engineering-related queries"""
        query = state["user_query"]
        print(f"Engineer agent received query: {query}")
        vector_store = state.get("vector_store")
        
        # Get PDF context if available
        pdf_context = ""
        has_pdf_content = False
        if vector_store:
            try:
                pdf_context = vector_store.search_pdf_knowledge(query, "engineering", "default", top_k=3)
                # Check if we actually got useful content
                no_content_messages = [
                    "No relevant content found in engineering documents.",
                    "No relevant content found in documents.", 
                    "No PDF documents uploaded yet."
                ]
                if pdf_context and pdf_context.strip() and not any(msg in pdf_context for msg in no_content_messages):
                    has_pdf_content = True
                    print(f"Engineer: Found PDF content for query: {query}")
                else:
                    print(f"Engineer: No relevant PDF content found for query: {query}")
            except Exception as e:
                print(f"Engineer: Error searching PDFs: {e}")
                pdf_context = ""
        
        # Generate response based on whether we have PDF content
        if not has_pdf_content:
            engineer_response = f"I don't have any relevant engineering documentation to answer your question about \"{query}\". Please upload engineering PDFs (technical docs, programming guides, etc.) so I can provide specific answers based on your documents."
        else:
            engineer_prompt = f"""
            You are a senior software engineer with expertise in programming, system design, DevOps, and technical solutions. Answer the question based ONLY on the following uploaded documentation:
            
            Engineering Documentation: {pdf_context}
            
            Question: {query}
            
            Important: 
            - Only use information from the provided documentation
            - If the documentation doesn't contain enough information to answer the question completely, say so
            - Provide practical, actionable advice when possible
            - Include relevant code examples or technical details from the documentation
            
            Return your response in JSON format with this exact structure:
            {{"response": "Your detailed answer here"}}
            """
            
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": engineer_prompt}],
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            try:
                import json
                result = json.loads(response.choices[0].message.content)
                engineer_response = result.get("response", response.choices[0].message.content)
            except:
                engineer_response = response.choices[0].message.content
        
        state["agent_response"] = engineer_response
        return state
    
    def doctor_agent(self, state: AgentState) -> AgentState:
        """Handle medical-related queries"""
        query = state["user_query"]
        print(f"Doctor agent received query: {query}")
        vector_store = state.get("vector_store")
        
        # Get PDF context if available
        pdf_context = ""
        has_pdf_content = False
        if vector_store:
            try:
                pdf_context = vector_store.search_pdf_knowledge(query, "medical", "default", top_k=3)
                
                # Check if we actually got useful content
                no_content_messages = [
                    "No relevant content found in medical documents.",
                    "No relevant content found in documents.", 
                    "No PDF documents uploaded yet."
                ]
                if pdf_context and pdf_context.strip() and not any(msg in pdf_context for msg in no_content_messages):
                    has_pdf_content = True
                    print(f"Doctor: Found PDF content for query: {query}")
                else:
                    print(f"Doctor: No relevant PDF content found for query: {query}")
            except Exception as e:
                print(f"Doctor: Error searching PDFs: {e}")
                pdf_context = ""
        
        # Generate response based on whether we have PDF content
        if not has_pdf_content:
            doctor_response = f"I don't have any relevant medical documentation to answer your question about '{query}'. Please upload medical PDFs (research papers, clinical guides, etc.) so I can provide specific answers based on your medical documents."
        else:
            doctor_prompt = f"""
            You are a medical expert with knowledge in health, medical procedures, anatomy, diseases, and treatments. Answer the question based ONLY on the following uploaded medical documentation:
            
            Medical Documentation: {pdf_context}
            
            Question: {query}
            
            Important: 
            - Only use information from the provided medical documentation
            - If the documentation doesn't contain enough information to answer the question completely, say so
            - Provide educational information while emphasizing the need for professional medical consultation
            - Include relevant details from the medical literature when available
            
            Return your response in JSON format with this exact structure:
            {{"response": "Your detailed answer here"}}
            """
            
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": doctor_prompt}],
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            try:
                import json
                result = json.loads(response.choices[0].message.content)
                doctor_response = result.get("response", response.choices[0].message.content)
            except:
                doctor_response = response.choices[0].message.content
        
        state["agent_response"] = doctor_response
        return state
    
    def lawyer_agent(self, state: AgentState) -> AgentState:
        """Handle legal-related queries"""
        query = state["user_query"]
        print(f"Lawyer agent received query: {query}")
        vector_store = state.get("vector_store")
        
        # Get PDF context if available
        pdf_context = ""
        has_pdf_content = False
        if vector_store:
            try:
                pdf_context = vector_store.search_pdf_knowledge(query, "legal", "default", top_k=3)
                # Check if we actually got useful content
                no_content_messages = [
                    "No relevant content found in legal documents.",
                    "No relevant content found in documents.", 
                    "No PDF documents uploaded yet."
                ]
                if pdf_context and pdf_context.strip() and not any(msg in pdf_context for msg in no_content_messages):
                    has_pdf_content = True
                    print(f"Lawyer: Found PDF content for query: {query}")
                else:
                    print(f"Lawyer: No relevant PDF content found for query: {query}")
            except Exception as e:
                print(f"Lawyer: Error searching PDFs: {e}")
                pdf_context = ""
        
        # Generate response based on whether we have PDF content
        if not has_pdf_content:
            lawyer_response = f"I don't have any relevant legal documentation to answer your question about '{query}'. Please upload legal PDFs (contracts, legal guides, court documents, etc.) so I can provide specific answers based on your legal documents."
        else:
            lawyer_prompt = f"""
            You are a legal expert with knowledge in law, contracts, legal procedures, regulations, and legal advice. Answer the question based ONLY on the following uploaded legal documentation:
            
            Legal Documentation: {pdf_context}
            
            Question: {query}
            
            Important: 
            - Only use information from the provided legal documentation
            - If the documentation doesn't contain enough information to answer the question completely, say so
            - Provide general guidance while emphasizing the need for professional legal consultation
            - Include relevant legal precedents or regulations from the documentation when available
            
            Return your response in JSON format with this exact structure:
            {{"response": "Your detailed answer here"}}
            """
            
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": lawyer_prompt}],
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            try:
                import json
                result = json.loads(response.choices[0].message.content)
                lawyer_response = result.get("response", response.choices[0].message.content)
            except:
                lawyer_response = response.choices[0].message.content
        
        state["agent_response"] = lawyer_response
        return state
    
    def route_to_agent(self, state: AgentState) -> str:
        """Route to the appropriate agent based on classification"""
        return state["selected_agent"]
    
    def create_graph(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("classifier", self.classify_query)
        workflow.add_node("engineer", self.engineer_agent)
        workflow.add_node("doctor", self.doctor_agent)
        workflow.add_node("lawyer", self.lawyer_agent)
        
        # Set entry point
        workflow.set_entry_point("classifier")
        
        # Add conditional routing
        workflow.add_conditional_edges(
            "classifier",
            self.route_to_agent,
            {
                "engineer": "engineer",
                "doctor": "doctor", 
                "lawyer": "lawyer"
            }
        )
        
        # Add end edges
        workflow.add_edge("engineer", END)
        workflow.add_edge("doctor", END)
        workflow.add_edge("lawyer", END)
        
        return workflow.compile()
    
    def process_query(self, user_query: str, vector_store=None) -> Dict[str, Any]:
        """Process a user query through the multi-agent system"""
        initial_state = {
            "messages": [],
            "user_query": user_query,
            "selected_agent": "",
            "agent_response": "",
            "specialist_field": "",
            "vector_store": vector_store
        }
        
        print(f"Processing query: {user_query}")
        result = self.graph.invoke(initial_state)
        print(f"Query processed. Selected agent: {result['selected_agent']}")
        
        return {
            "query": user_query,
            "selected_agent": result["selected_agent"],
            "specialist_field": result["specialist_field"],
            "response": result["agent_response"]
        }
    
    def visualize_graph_ascii(self):
        """Print ASCII representation of the graph"""
        print("Multi-Agent System Graph Structure (ASCII):")
        print("=" * 50)
        try:
            ascii_graph = self.graph.get_graph().draw_ascii()
            print(ascii_graph)
        except Exception as e:
            print(f"Error generating ASCII graph: {e}")
            print("Note: ASCII visualization might not be available in all LangGraph versions")
    
    def visualize_graph_mermaid(self):
        """Generate Mermaid diagram representation of the graph"""
        print("Multi-Agent System Graph Structure (Mermaid):")
        print("=" * 50)
        try:
            mermaid_graph = self.graph.get_graph().draw_mermaid()
            print(mermaid_graph)
            return mermaid_graph
        except Exception as e:
            print(f"Error generating Mermaid graph: {e}")
            print("Note: Mermaid visualization might not be available in all LangGraph versions")
            return None
    
    def visualize_graph_png(self, filename="multiagent_graph.png"):
        """Generate PNG image of the graph (requires graphviz)"""
        try:
            # Generate PNG image
            png_data = self.graph.get_graph().draw_mermaid_png()
            
            # Save to file
            with open(filename, "wb") as f:
                f.write(png_data)
            
            print(f"Graph visualization saved as '{filename}'")
            
            # Display in Jupyter if available
            try:
                display(Image(filename))
            except:
                print(f"PNG saved to {filename}. Open the file to view the graph visualization.")
                
        except Exception as e:
            print(f"Error generating PNG graph: {e}")
            print("Note: PNG visualization requires graphviz to be installed.")
            print("Install with: pip install graphviz or apt-get install graphviz")
    
    def show_all_visualizations(self):
        """Display all available graph visualizations"""
        print("Multi-Agent System Graph Visualizations")
        print("=" * 60)
        
        # ASCII representation
        self.visualize_graph_ascii()
        print("\n")
        
        # Mermaid representation  
        self.visualize_graph_mermaid()
        print("\n")
        
        # PNG representation
        self.visualize_graph_png() 
