
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ----------------------------------------------------------------------------
# 1) Model path
# ----------------------------------------------------------------------------
# Set the local path of your model (make sure this directory contains
# your model's 'config.json', 'pytorch_model.bin', and tokenizer files).
model_path = "/home/user/models/Llama-3.2-3B-Instruct"

# ----------------------------------------------------------------------------
# 2) Load the tokenizer
# ----------------------------------------------------------------------------
# If you're using a LLaMA-based model, ensure your Transformers version
# supports it, or use the correct tokenizer (LlamaTokenizer).
tokenizer = AutoTokenizer.from_pretrained(model_path)

# ----------------------------------------------------------------------------
# 3) Choose a device
# ----------------------------------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

# ----------------------------------------------------------------------------
# 4) Load the model
# ----------------------------------------------------------------------------
# Option A: Use device_map="auto" (requires accelerate >= 0.15 and
#           transformers >= 4.30 for automatic sharding).
#           This places different layers on different GPUs if available.
# Option B: Move the model manually to the device with `.to(device)`.
#           Do not combine both approaches, or it can cause conflicts.
#
# Below is an example with device_map="auto". If you only have one GPU
# or a CPU, you can remove device_map="auto" and simply do .to(device).
# ----------------------------------------------------------------------------

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float32,
    device_map="auto"
)
# If you prefer manual placement on a single device, use:
#   model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32).to(device)

# ----------------------------------------------------------------------------
# 5) Define a chat function
# ----------------------------------------------------------------------------
def chat(query: str) -> str:
    # Tokenize input
    inputs = tokenizer(query, return_tensors="pt").to(device)

    # Generate text with the model
    with torch.no_grad():
        # You can tune max_new_tokens, do_sample, top_p, temperature, etc. for better responses
        output_tokens = model.generate(**inputs, max_new_tokens=150)
    
    # Decode the tokens
    response = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
    return response

# ----------------------------------------------------------------------------
# 6) Test the chat function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    query = "Why did my Kubernetes pod crash?"
    response = chat(query)
    print("Model Response:", response)
