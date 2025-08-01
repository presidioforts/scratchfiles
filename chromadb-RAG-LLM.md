# orchestrator.py
from fastapi import FastAPI
from pydantic import BaseModel
import httpx, textwrap, os

RAG_URL   = os.getenv("RAG_URL",   "http://localhost:7000/retrieve")
LLM_URL   = os.getenv("LLM_URL",   "http://localhost:7001/generate")
TOP_K     = int(os.getenv("TOP_K", 6))

SYSTEM = (
    "You are a senior DevOps assistant. "
    "Answer concisely with exact fix steps, citing sources like [#1]."
)

app = FastAPI()
client = httpx.AsyncClient(timeout=30)

class AskReq(BaseModel):
    question: str

@app.post("/ask")
async def ask(req: AskReq):
    # 1) Retrieve docs
    r = await client.post(RAG_URL, json={"query": req.question, "k": TOP_K})
    r.raise_for_status()
    docs = r.json()["docs"]

    # 2) Build prompt
    ctx = "\n\n".join([f"[#{i+1}] {textwrap.shorten(d, 300)}"
                       for i, d in enumerate(docs)])
    prompt = f"{SYSTEM}\n\nContext:\n{ctx}\n\nQuestion: {req.question}"

    # 3) Generate answer
    g = await client.post(LLM_URL, json={"prompt": prompt})
    g.raise_for_status()
    answer = g.json()["text"]

    return {"answer": answer, "sources": list(range(1, len(docs)+1))}
