Your current training code is structured well for fine-tuning LLaMA 3.2 Instruct 1B using **LoRA (Low-Rank Adaptation)**, but it only supports **single-sample training**. Below, I'll update it to **load multiple examples from `batch_data.json`**, ensuring proper batching for effective training.

---

### **Key Fixes & Enhancements**
✔ **Support for Batch Training:** Reads multiple examples from `batch_data.json`.  
✔ **Improved Data Loading:** `JSONDataset` class reads all issues and resolutions.  
✔ **Fine-Tuning Multiple Epochs:** Adjusts for batch training efficiency.  
✔ **Training Progress Logging:** Displays loss per batch.  
✔ **CPU Optimizations:** Ensures it works on a CPU-based VM.  

---

### **Updated Training Code for Multiple Examples**

```python
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

# -------------------------------------------------------------------
# 1) LOAD DATASET FROM JSON FILE
# -------------------------------------------------------------------
DATA_PATH = "batch_data.json"
with open(DATA_PATH, "r") as f:
    json_data = json.load(f)

# Define a prompt format for training
PROMPT_TEMPLATE = (
    "<|begin_of_text|>\n"
    "Issue: {issue}\n"
    "Resolution: {resolution}\n"
    "<|end_of_text|>"
)


# -------------------------------------------------------------------
# 2) CREATE DATASET CLASS TO HANDLE MULTIPLE EXAMPLES
# -------------------------------------------------------------------
class JSONDataset(Dataset):
    def __init__(self, data):
        super().__init__()
        self.samples = [
            PROMPT_TEMPLATE.format(issue=entry["issue"], resolution=entry["resolution"])
            for entry in data
        ]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


# -------------------------------------------------------------------
# 3) COLLATE FUNCTION (Tokenization)
# -------------------------------------------------------------------
def collate_fn(batch_texts):
    """
    Tokenizes the batch, ensuring 'labels' match 'input_ids' for causal LM.
    """
    encoding = tokenizer(
        batch_texts,
        padding="max_length",
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )
    encoding["labels"] = encoding["input_ids"].clone()
    return encoding


# -------------------------------------------------------------------
# 4) LOAD LLAMA MODEL & TOKENIZER
# -------------------------------------------------------------------
LOCAL_LLAMA_PATH = "./llama-3.2-1b"

print(f">>> Loading tokenizer from: {LOCAL_LLAMA_PATH}")
tokenizer = AutoTokenizer.from_pretrained(LOCAL_LLAMA_PATH)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print(f">>> Loading base LLaMA model from: {LOCAL_LLAMA_PATH}")
base_model = AutoModelForCausalLM.from_pretrained(LOCAL_LLAMA_PATH)


# -------------------------------------------------------------------
# 5) APPLY LoRA ADAPTERS
# -------------------------------------------------------------------
print(">>> Applying LoRA adapters...")
lora_config = LoraConfig(
    r=8,  # Lower rank to fit better on CPU
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(base_model, lora_config)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.train()


# -------------------------------------------------------------------
# 6) BUILD DATASET & DATALOADER
# -------------------------------------------------------------------
print(">>> Building dataset from JSON file...")
dataset = JSONDataset(json_data)
dataloader = DataLoader(
    dataset,
    batch_size=2,  # Adjust for efficiency
    shuffle=True,
    collate_fn=collate_fn
)

print(f">>> Loaded {len(dataset)} training examples.")

# -------------------------------------------------------------------
# 7) TRAINING LOOP
# -------------------------------------------------------------------
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)  # Lower LR for stability
EPOCHS = 3  # Train over multiple epochs to reinforce learning

print(">>> Starting training...")
for epoch in range(EPOCHS):
    print(f"\n=== Epoch {epoch + 1}/{EPOCHS} ===")
    total_loss = 0
    for step, batch in enumerate(dataloader):
        for k in batch:
            batch[k] = batch[k].to(device)

        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        optimizer.zero_grad()

        total_loss += loss.item()
        if step % 2 == 0:
            print(f"Step {step}, Loss = {loss.item():.4f}")

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch + 1} completed. Average Loss: {avg_loss:.4f}")


# -------------------------------------------------------------------
# 8) SAVE LoRA-TUNED MODEL
# -------------------------------------------------------------------
OUTPUT_DIR = "./batch_finetuned_llama"
print(f">>> Saving model & tokenizer to: {OUTPUT_DIR}")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(">>> Training complete! Model saved.")
```

---

### **🔧 Key Enhancements**
1. **Batch Training from JSON**  
   - Reads multiple issue-resolution pairs from `batch_data.json`.
   - Uses `JSONDataset` to handle multiple samples.

2. **Fine-Tuning LoRA on CPU**  
   - Uses **LoRA rank=8** (previously 16) to reduce memory.
   - Keeps `target_modules=["q_proj", "v_proj"]`, standard for LLaMA.

3. **Training Loop Optimizations**  
   - **Epochs increased to 3** to allow better learning.  
   - **Lower learning rate (2e-5)** to stabilize fine-tuning.  
   - **Batch size set to 2** (tunable based on available memory).  

4. **Performance Logging**  
   - Displays **loss per batch**.
   - Shows **epoch progress** and final **average loss**.

---

### **Next Steps 🚀**
✅ **Run the script on your CPU VM.**  
✅ **Validate responses:** Load the model and test inference.  
✅ **Deploy API:** Use FastAPI to serve the fine-tuned model.  

Would you like an **inference script** to test the fine-tuned model? 🚀
