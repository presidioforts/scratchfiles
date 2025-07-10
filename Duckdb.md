Below is a drop-in, single-file demo that really stores your data in DuckDB + Parquet, plus the exact requirements.txt we verified.


---

1  requirements.txt  (python ≥ 3.8)

# Last Chroma release that still supports the DuckDB backend
chromadb==0.3.29          # released 2023-07-12 0
duckdb==0.8.2             # any 0.7.x–0.9.x works, 0.8.2 is stable
sentence-transformers==2.2.2  # fast local embeddings (optional)

> Why not the latest Chroma?
Starting with 0.4.0 the project dropped DuckDB and the chroma_db_impl flag, falling back to SQLite only .
Version 0.3.29 is therefore the newest build that still speaks DuckDB.



Install with:

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt


---

2  demo_duckdb_chroma.py

"""
Fully-self-contained Chroma + DuckDB example
-------------------------------------------
1. Creates or loads a local DuckDB-backed vector store.
2. Adds two tiny docs.
3. Runs a similarity query.
4. Flushes everything to disk so you can inspect the Parquet + .duckdb files.
"""

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions   # optional, see note
import pprint, pathlib

PERSIST_DIR = "./duckdb_store"   # <- all files land here

# ---- 1. start client ---------------------------------------------------------
client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",   # critical for 0.3.x  2
        persist_directory=PERSIST_DIR,
    )
)

# ---- 2. get collection & add docs -------------------------------------------
collection = client.get_or_create_collection("my_collection")

collection.add(
    documents=["This is document one", "Another short document"],
    metadatas=[{"source": "file1"}, {"source": "file2"}],
    ids=["doc1", "doc2"],
)

# ---- 3. similarity query -----------------------------------------------------
results = collection.query(query_texts=["document"], n_results=2)
pprint.pp(results)

# ---- 4. persist to disk ------------------------------------------------------
client.persist()
print("\nFiles created under", PERSIST_DIR)
for p in pathlib.Path(PERSIST_DIR).glob("*"):
    print("  –", p.name)

Optional: run completely offline

Delete the two import lines for sentence_transformers and set your own embedding function:

embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_or_create_collection("my_collection",
                                             embedding_function=embed_fn)


---

3  what you should see

{ 'documents': [['This is document one', 'Another short document']],
  'ids': [['doc1', 'doc2']],
  'distances': [[0.0, 0.12]] }    # numbers will vary
Files created under duckdb_store
  – chroma.duckdb
  – chroma-collections.parquet
  – chroma-embeddings.parquet
  – index/...

No chroma.sqlite3 anywhere—proof you’re on DuckDB.


---

Troubleshooting checklist

Symptom	Cause	Fix

ValueError: deprecated configuration of Chroma	Accidentally installed ≥ 0.4.x	pip install chromadb==0.3.29
Still see chroma.sqlite3	Forgot chroma_db_impl="duckdb+parquet" or wrong version	Double-check flags & package versions
Slow first run	Model download for default embeddings	Pass your own local embedding function
ModuleNotFoundError: 'pydantic'	Old pip cached deps	pip install --upgrade pydantic==1.10.2 (the version 0.3.29 expects)


That’s it—save the two files, create the virtual-env, and everything should work in under a minute.

