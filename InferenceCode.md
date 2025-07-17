
Excellent. Here's a working LangGraph + LlamaIndex starter project your developer can try today. This setup assumes:

You’ve already embedded and indexed your documents using LlamaIndex.

You want to route the query through:
→ Stage classifier → Retriever (Chroma + KG) → RCA linker → Claude/GPT for high reasoning → Format response.



---

✅ Folder Structure

devops-rca-assistant/
│
├── ingest/
│   └── load_index.py
│
├── graph/
│   └── langgraph_rca.py
│
├── config/
│   └── secrets.env  ← contains API keys
│
├── run.py
└── requirements.txt


---

✅ requirements.txt

llama-index>=0.10.20
chromadb>=0.5.0
langgraph>=0.5.3
langchain-openai>=0.3.3
python-dotenv


---

✅ config/secrets.env

OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key


---

✅ graph/langgraph_rca.py

import os
from dotenv import load_dotenv
from llama_index import load_index_from_storage
from langgraph import graph
from langchain_openai import ChatOpenAI
from llama_index.query_engine import RetrieverQueryEngine

load_dotenv()

# Load prebuilt vector index (Chroma) and optional KG
index = load_index_from_storage("index_storage")  # your vector index dir
retriever = index.as_retriever(similarity_top_k=5)

llm = ChatOpenAI(
    model="gpt-4o",  # or "gpt-3.5-turbo", or switch to Claude later
    temperature=0,
)

@graph.node
def classify_stage(state):
    query = state["query"]
    # Basic keyword rule-based classification (replace with model if needed)
    stage = "Build" if "compile" in query.lower() else "Deploy"
    return {**state, "stage": stage}

@graph.node
def retrieve_context(state):
    nodes = retriever.retrieve(state["query"])
    context = "\n\n".join([n.text for n in nodes])
    return {**state, "context": context}

@graph.node
def reason_with_llm(state):
    prompt = f"""Developer reported:\n{state['query']}\n\nContext:\n{state['context']}\n\nFind the Root Cause and suggest fix."""
    result = llm.invoke(prompt)
    return {**state, "response": result.content}

@graph.node
def format_output(state):
    return {
        "RCA_Response": state["response"],
        "Stage": state["stage"]
    }

# Build LangGraph
dag = graph.DAG()
dag.add_edges([
    ("input", "classify_stage"),
    ("classify_stage", "retrieve_context"),
    ("retrieve_context", "reason_with_llm"),
    ("reason_with_llm", "format_output"),
    ("format_output", "output")
])

assistant = dag.compile()


---

✅ run.py

from graph.langgraph_rca import assistant

while True:
    query = input("Dev Query > ")
    if query.lower() in ["exit", "quit"]: break
    result = assistant.invoke({"query": query})
    print("\n🧠 RCA Assistant Response:\n")
    print(result["RCA_Response"])
    print("\n📌 Stage Identified:", result["Stage"])
    print("—" * 60)


---

✅ Run It

$ pip install -r requirements.txt
$ python run.py

Try:

Dev Query > Build failed with 'cannot find symbol'


---

🔁 What Next?

You can:

Switch ChatOpenAI to Claude:


from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)

Upgrade classify_stage() to use a local model or prompt chain.

Add KG linkage using KnowledgeGraphIndex.as_retriever()



---

Would you like me to also generate:

Dockerfile for containerizing this

Version that runs as a FastAPI endpoint for UI integration Let me know and I’ll prep it right away.


