
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

# =====================================================
# 1) CONFIG
# =====================================================
LOCAL_LLAMA_PATH = "./llama-3.2-1b"     # Path to your local LLaMA checkpoint
JSON_PATH = "issues_resolutions.json"  # JSON file with a list of objects
OUTPUT_DIR = "./finetuned_llama"

# Hyperparameters
BATCH_SIZE = 2
EPOCHS = 3
LEARNING_RATE = 1e-4
MAX_SEQ_LEN = 128

# Prompt template
PROMPT_TEMPLATE = (
    "<|begin_of_text|>\n"
    "Issue: {issue}\n"
    "Resolution: {resolution}\n"
    "<|end_of_text|>"
)

# =====================================================
# 2) DATASET DEFINITION
# =====================================================
class JSONBatchDataset(Dataset):
    def __init__(self, json_file, prompt_template):
        super().__init__()
        self.data = []
        self.prompt_template = prompt_template
        
        # Read the entire JSON file into a list of objects
        with open(json_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)  # e.g. a list of {"issue": "...", "resolution": "..."}
        
        # Build the prompt text for each sample
        for entry in raw_data:
            issue_text = entry["issue"].strip()
            resolution_text = entry["resolution"].strip()
            
            prompt_text = self.prompt_template.format(
                issue=issue_text, 
                resolution=resolution_text
            )
            self.data.append(prompt_text)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# =====================================================
# 3) COLLATE FUNCTION
# =====================================================
def collate_fn(batch_texts):
    """
    Tokenizes a batch of strings, then sets labels = input_ids for causal LM.
    """
    encoding = tokenizer(
        batch_texts,
        padding="max_length",
        truncation=True,
        max_length=MAX_SEQ_LEN,
        return_tensors="pt"
    )
    encoding["labels"] = encoding["input_ids"].clone()
    return encoding

# =====================================================
# 4) LOAD TOKENIZER & MODEL
# =====================================================
if __name__ == "__main__":
    print(f"Loading tokenizer from: {LOCAL_LLAMA_PATH}")
    tokenizer = AutoTokenizer.from_pretrained(LOCAL_LLAMA_PATH)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"Loading base LLaMA model from: {LOCAL_LLAMA_PATH}")
    base_model = AutoModelForCausalLM.from_pretrained(LOCAL_LLAMA_PATH)

    # =====================================================
    # 5) APPLY LoRA
    # =====================================================
    print("Applying LoRA adapters...")
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],  # typical for LLaMA
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(base_model, lora_config)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.train()

    # =====================================================
    # 6) CREATE DATASET & DATALOADER
    # =====================================================
    print(f"Reading JSON data from: {JSON_PATH}")
    dataset = JSONBatchDataset(JSON_PATH, PROMPT_TEMPLATE)
    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,  # typical for training
        collate_fn=collate_fn
    )

    print(f"Total samples in dataset: {len(dataset)}")
    if len(dataset) > 0:
        print("Example prompt from dataset:", dataset[0])

    # =====================================================
    # 7) TRAINING LOOP
    # =====================================================
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

    print("Starting training...")
    for epoch in range(EPOCHS):
        print(f"=== Epoch {epoch+1}/{EPOCHS} ===")
        for step, batch in enumerate(dataloader):
            for k in batch:
                batch[k] = batch[k].to(device)

            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            if step % 1 == 0:
                print(f"Step {step}, Loss: {loss.item():.4f}")

    # =====================================================
    # 8) SAVE THE FINE-TUNED MODEL
    # =====================================================
    print(f"Saving model & tokenizer to: {OUTPUT_DIR}")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Done! Fine-tuned model is in:", OUTPUT_DIR)
