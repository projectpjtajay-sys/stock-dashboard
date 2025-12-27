from fastapi import FastAPI, Request
from pydantic import BaseModel
from graph_rag import get_rag_graph

app = FastAPI()
rag_graph = get_rag_graph()

class PromptInput(BaseModel):
    user_prompt: str

@app.post("/rag-query")
async def query_rag(input_data: PromptInput):
    state = {"user_prompt": input_data.user_prompt}
    result = rag_graph.invoke(state)
    return {"query": input_data.user_prompt, "answer": result["answer"]}
