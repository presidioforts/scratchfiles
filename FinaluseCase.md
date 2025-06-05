
Use Case Document: AI-Powered DevOps Knowledge Assistant using Sentence Transformer, ChromaDB, and LLaMA-3 3B

1. Objective

To build an AI-powered DevOps knowledge assistant that delivers accurate, up-to-date, and context-aware responses to developer and operations queries by leveraging internal CI/CD, infrastructure, and incident documentation. The system ensures that answers are strictly grounded in enterprise documents, minimizing hallucinations and maintaining full traceability.

2. System Overview

The assistant is designed using a Retrieval-Augmented Generation (RAG) architecture combining three core components:

Sentence Transformer (Embedding Layer): Converts user queries into high-quality embeddings for semantic search.

ChromaDB (Vector Store): Stores pre-computed embeddings of document chunks and retrieves relevant content based on query similarity.

LLaMA-3 3B Instruct (LLM Layer): Generates human-like answers by synthesizing the retrieved document chunks and user query.

3. Workflow

User Input: The DevOps engineer submits a natural language question (e.g., "Why did my Jenkins pipeline fail on step X?" or "How do I configure GitHub Actions cache for Node.js builds?").

Embedding: The query is encoded into a dense vector using the Sentence Transformer.

Retrieval: ChromaDB performs a semantic search and returns the top-k most relevant document chunks from runbooks, CI/CD pipeline guides, logs (Jenkins or GitHub Actions), FAQs, or past incidents.

Prompt Assembly: Retrieved chunks are formatted with the original question into a prompt.

Generation: LLaMA-3 3B generates a fluent and contextual answer using the prompt.

Response Delivery: The response, along with source citations, is delivered to the user.

4. Key Features

Factual Grounding:

All answers are generated based solely on the retrieved content from DevOps documentation.

Eliminates hallucinations and ensures output is aligned with enterprise workflows, runbooks, and policies.

Traceability:

Each response can be traced back to specific source documents (e.g., Jenkinsfile templates, GitHub Actions YAML configurations, CI logs).

Enhances trust, especially for incident resolution and RCA documentation.

Real-Time Adaptability:

No retraining of the LLM is required when documentation or runbooks change.

Updates are reflected immediately via retrieval from ChromaDB.

5. Benefits

✅ Accurate DevOps support grounded in verified internal documentation

✅ Low latency and cost-effective inference

✅ No LLM fine-tuning required for pipeline changes (Jenkins, GitHub Actions)

✅ Scalable and modular architecture aligned with DevOps tooling

✅ Improves SRE, platform engineering, and developer productivity

6. Recommended Configuration

Embedding Model: Custom fine-tuned Sentence Transformer (e.g., all-mpnet-base-v2)

Vector Store: ChromaDB in persistent mode (optional: PostgreSQL backend)

LLM Model: LLaMA-3 3B Instruct (quantized to Q6_K if needed for resource efficiency)

Chunking Strategy: ~350 tokens per chunk with 15% overlap

Top-K Retrieval: k = 10 → rerank → keep 3 for context

Context Window: Max 8,192 tokens (recommended), context length trimmed to fit prompt and question

7. Use Case Suitability

This architecture is ideal for:

Internal DevOps and platform service teams

CI/CD pipeline support automation for Jenkins and GitHub Actions

Incident triage assistants and RCA accelerators

Self-serve documentation for developers and SREs

AI copilots integrated into DevOps dashboards and chat tools

8. Conclusion

The combination of Sentence Transformer, ChromaDB, and LLaMA-3 3B delivers a cost-effective, scalable, and trustworthy AI assistant for DevOps use cases. It provides accurate answers grounded in real operational knowledge, across both Jenkins and GitHub Actions ecosystems, with minimal overhead and high adaptability—making it ideal for developer productivity, incident response, and infrastructure automation.

