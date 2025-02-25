import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

# -------------------------------------------------------------------
# 1) SINGLE (ISSUE, RESOLUTION) PAIR  (No JSON File)
# -------------------------------------------------------------------
issue_text = "Build failed due to missing dependency."
resolution_text = "Please add package X to requirements.txt and rebuild."

# A minimal prompt template to unify the text
PROMPT_TEMPLATE = (
    "<|begin_of_text|>\n"
    "Issue: {issue}\n"
    "Resolution: {resolution}\n"
    "<|end_of_text|>"
)


# -------------------------------------------------------------------
# 2) A TINY DATASET (Returns Just One Prompt String)
# -------------------------------------------------------------------
class SingleSampleDataset(Dataset):
    def __init__(self, issue, resolution):
        super().__init__()
        self.prompt_text = PROMPT_TEMPLATE.format(issue=issue, resolution=resolution)

    def __len__(self):
        # Only 1 sample
        return 1

    def __getitem__(self, idx):
        # Always return the same prompt string
        return self.prompt_text


# -------------------------------------------------------------------
# 3) COLLATE FUNCTION (Tokenize & Create Labels)
# -------------------------------------------------------------------
def collate_fn(batch_texts):
    """
    - batch_texts is a list of strings (here, length=1).
    - We tokenize, set 'labels' = 'input_ids' for causal LM training.
    """
    encoding = tokenizer(
        batch_texts,
        padding="max_length",
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )
    # For causal LM, set labels = input_ids
    encoding["labels"] = encoding["input_ids"].clone()
    return encoding


# -------------------------------------------------------------------
# 4) LOAD LLAMA MODEL & TOKENIZER
# -------------------------------------------------------------------
LOCAL_LLAMA_PATH = "./llama-3.2-1b"  # Adjust if needed

print(f">>> Loading tokenizer from: {LOCAL_LLAMA_PATH}")
tokenizer = AutoTokenizer.from_pretrained(LOCAL_LLAMA_PATH)
# If tokenizer has no PAD token, point it to EOS
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print(f">>> Loading base LLaMA model from: {LOCAL_LLAMA_PATH}")
base_model = AutoModelForCausalLM.from_pretrained(LOCAL_LLAMA_PATH)


# -------------------------------------------------------------------
# 5) PREPARE LoRA CONFIG & WRAP MODEL
# -------------------------------------------------------------------
print(">>> Applying LoRA adapters...")
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj","v_proj"],  # typical for LLaMA
    lora_dropout=0.05,
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
print(">>> Building single-sample dataset...")
dataset = SingleSampleDataset(issue_text, resolution_text)
dataloader = DataLoader(
    dataset,
    batch_size=1,
    shuffle=False,
    collate_fn=collate_fn
)

# Debug: Show the single example
print("Example prompt text:", dataset[0])

# -------------------------------------------------------------------
# 7) TRAINING LOOP
# -------------------------------------------------------------------
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
EPOCHS = 1  # Just 1 epoch for demonstration

print(">>> Starting training on single sample...")
for epoch in range(EPOCHS):
    print(f"=== Epoch {epoch} ===")
    for step, batch in enumerate(dataloader):
        for k in batch:
            batch[k] = batch[k].to(device)

        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        optimizer.zero_grad()

        print(f"Step {step}, loss = {loss.item():.4f}")

# -------------------------------------------------------------------
# 8) SAVE LoRA-TUNED MODEL
# -------------------------------------------------------------------
OUTPUT_DIR = "./single_sample_llama"
print(f">>> Saving model & tokenizer to: {OUTPUT_DIR}")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(">>> Done! You have a LoRA-updated LLaMA (trained on one sample).")
