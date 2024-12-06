from huggingface_hub import HfApi, snapshot_download
import os

# Set Hugging Face endpoint and token
os.environ["HF_ENDPOINT"] = "https://your-private-hub-instance"
HF_TOKEN = "your_hf_token_here"

# Specify the model repo
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Use the token and custom endpoint to download the model
model_dir = snapshot_download(
    repo_id=model_name,
    use_auth_token=HF_TOKEN,
    cache_dir="./local_model_cache"
)

print(f"Model downloaded to: {model_dir}")

# Example: Load the downloaded model with SentenceTransformers
from sentence_transformers import SentenceTransformer

# Load model from local cache
sentence_model = SentenceTransformer(model_dir)

# Test the model
sentences = ["This is an example sentence.", "Each sentence is converted."]
embeddings = sentence_model.encode(sentences)
print("Embeddings Shape:", embeddings.shape)
