from langgraph.graph import StateGraph, END
from typing import TypedDict
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from ingest import build_or_load_index

class RAGState(TypedDict):
    user_prompt: str
    answer: str

def retrieve_answer(state: RAGState) -> RAGState:
    query = state["user_prompt"]
    index = build_or_load_index()

    retriever = VectorIndexRetriever(index=index)
    engine = RetrieverQueryEngine(retriever=retriever)

    response = engine.query(query)
    return {"user_prompt": query, "answer": str(response)}

def get_rag_graph():
    builder = StateGraph(RAGState) 
    builder.add_node("RAGRetriever", retrieve_answer)
    builder.set_entry_point("RAGRetriever")
    builder.add_edge("RAGRetriever", END)
    return builder.compile()
