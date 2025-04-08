#!/usr/bin/env python3
import os
import pdfplumber
import nltk
import numpy as np
import faiss
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

# --- NLTK Setup: Download tokenizers if not present ---
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


# --- 1. Extract text from PDF ---
def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF using pdfplumber.
    Returns a single string.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# --- 2. Chunk text into groups of sentences ---
def chunk_text(text, max_chunk_size=500):
    """
    Splits text into chunks of up to max_chunk_size characters,
    based on sentence boundaries. If a single sentence is longer
    than max_chunk_size, it will be placed in its own chunk
    (and may exceed the limit).
    """
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


# --- 3. Load or Save Model ---
def load_or_save_model(model_path="my_local_model", hf_model_name="all-MiniLM-L6-v2"):
    """
    Loads the SentenceTransformer model from model_path if it exists.
    Otherwise, downloads the model from Hugging Face Hub and saves locally.
    """
    if os.path.exists(model_path):
        model = SentenceTransformer(model_path)
    else:
        model = SentenceTransformer(hf_model_name)
        model.save(model_path)
    return model


# --- 4. Build or Load Embeddings ---
def build_or_load_embeddings(chunks, model, embedding_file="chunk_embeddings.npy", text_file="text_chunks.txt"):
    """
    If embedding_file and text_file do not exist, encode the chunks and save them.
    Otherwise, load them from disk.
    Returns: (embeddings, chunks) where `chunks` is the list of text chunks.
    """
    if not os.path.exists(embedding_file) or not os.path.exists(text_file):
        print("🧠 Encoding chunks with SentenceTransformer...")
        embeddings = model.encode(chunks, show_progress_bar=True)

        np.save(embedding_file, embeddings)

        with open(text_file, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(chunk + "\n---\n")

        return embeddings, chunks
    else:
        print("✅ Embedding files found. Loading from disk...")
        embeddings = np.load(embedding_file)

        with open(text_file, "r", encoding="utf-8") as f:
            saved_chunks = f.read().split("\n---\n")

        return embeddings, saved_chunks


# --- 5. Build FAISS Index ---
def build_faiss_index(embeddings):
    """
    Builds a simple FAISS IndexFlatL2 index from the given embeddings.
    Returns the index.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


# --- 6. Answer Queries ---
def answer_query(query, model, index, chunks, top_k=3):
    """
    Encodes the query using the model, searches in the FAISS index,
    and returns the top_k chunk results (plus distances).
    """
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        results.append((chunks[idx], dist))
    return results


# --- 7. Main Execution ---
if __name__ == "__main__":
    pdf_file = "user_guide.pdf"  # or the path to your PDF

    # 1) Extract text
    print("Extracting text from PDF...")
    raw_text = extract_text_from_pdf(pdf_file)

    # 2) Chunk text
    print("Splitting text into chunks...")
    chunks = chunk_text(raw_text, max_chunk_size=500)

    # 3) Load or save the model locally
    model = load_or_save_model(model_path="my_local_model", hf_model_name="all-MiniLM-L6-v2")

    # 4) Build or load embeddings
    embeddings, chunks = build_or_load_embeddings(chunks, model,
                                                  embedding_file="chunk_embeddings.npy",
                                                  text_file="text_chunks.txt")

    # 5) Build FAISS index
    print("Building FAISS index...")
    index = build_faiss_index(embeddings)

    # Optional: persist the index to disk if you wish
    # if not os.path.exists("faiss_index.index"):
    #     faiss.write_index(index, "faiss_index.index")
    # else:
    #     index = faiss.read_index("faiss_index.index")

    # 6) Interactive GPT-like loop
    print("\nThe system is ready. Type 'exit' or 'quit' to leave.")
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Assistant: Exiting. Goodbye!")
            break

        # Search FAISS for relevant chunks
        results = answer_query(user_input, model, index, chunks, top_k=3)

        # Format an "Assistant" style response
        # You might want to process the results more or pass them to a summarizer.
        response_str = "\nAssistant:\n"
        for idx, (chunk_text, distance) in enumerate(results, start=1):
            response_str += f"  [{idx}] {chunk_text}\n      (distance: {distance:.4f})\n\n"

        print(response_str)
