
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JFrog configuration from environment variables
JFROG_URL = os.getenv("JFROG_URL")
OUTPUT_DIR = "./local-all-mpnet-base"
JFROG_USERNAME = os.getenv("JFROG_USERNAME")
JFROG_PASSWORD = os.getenv("JFROG_PASSWORD")

# Model files required for SentenceTransformer
MODEL_FILES = [
    "config.json",
    "pytorch_model.bin",
    "tokenizer_config.json",
    "vocab.txt"
]

def download_file(file_url, output_path, auth):
    """
    Downloads a file from the specified URL to the output path.

    Args:
        file_url (str): The URL of the file to download.
        output_path (str): The local path where the file should be saved.
        auth (tuple): Authentication tuple (username, password/token).

    Returns:
        bool: True if the download succeeds, False otherwise.
    """
    try:
        response = requests.get(file_url, auth=auth, timeout=30)
        if response.status_code == 200:
            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {os.path.basename(output_path)}")
            return True
        else:
            print(f"Failed to download {file_url}. HTTP Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {file_url}: {e}")
        return False

def download_model():
    """
    Downloads the required model files from the JFrog repository.
    """
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Download each file
    auth = (JFROG_USERNAME, JFROG_PASSWORD)
    for file_name in MODEL_FILES:
        file_url = f"{JFROG_URL}/{file_name}"
        output_path = os.path.join(OUTPUT_DIR, file_name)
        if not download_file(file_url, output_path, auth):
            print(f"Error: Could not download {file_name}. Aborting!")
            return False
    print("All files downloaded successfully!")
    return True

if __name__ == "__main__":
    # Step 1: Download the model
    if download_model():
        print("Model is ready for use in:", OUTPUT_DIR)

        # Step 2: Use the model with SentenceTransformers
        try:
            from sentence_transformers import SentenceTransformer

            # Load the model
            print("Loading the model...")
            model = SentenceTransformer(OUTPUT_DIR)

            # Test the model
            sentences = ["This is a test sentence.", "Another example sentence."]
            embeddings = model.encode(sentences)
            print("Embedding shape:", embeddings.shape)
            print("Embeddings:", embeddings)
        except Exception as e:
            print(f"Error using the model: {e}")
