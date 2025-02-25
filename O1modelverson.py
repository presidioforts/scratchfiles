import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, PeftModel

# -----------------------------
# Configuration
# -----------------------------
local_model_path = "/path/to/llama-3.2-1b"  # Adjust to your local model directory
dataset_path = "issues_resolutions.json"    # Path to your local JSON dataset
output_dir = "./finetuned_model"            # Directory to save the fine-tuned model

# Prompt template (adjust if needed)
prompt_template = (
    "<|begin_of_text|><|start_header_id|>user<|end_header_id>\n"
    "Issue: {issue}\n"
    "Resolution: <|eot_id|><|start_header_id|>assistant<|end_header_id>\n"
    "{resolution}<|eot_id|>"
)

# -----------------------------
# Load tokenizer & model
# -----------------------------
tokenizer = AutoTokenizer.from_pretrained(local_model_path)

if os.path.exists(output_dir) and os.path.isdir(output_dir):
    # Load an already fine-tuned model (resume)
    print(f"Loading existing fine-tuned model from {output_dir}")
    base_model = AutoModelForCausalLM.from_pretrained(local_model_path)
    model = PeftModel.from_pretrained(base_model, output_dir)
else:
    # Load base model from local directory
    print(f"Loading base model from {local_model_path}")
    model = AutoModelForCausalLM.from_pretrained(local_model_path)
    
    # Configure LoRA
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],  # for LLaMA-like models
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # Wrap the base model with the LoRA adapter
    model = get_peft_model(model, lora_config)

# If pad token is not set, align it to eos_token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# -----------------------------
# Load and process dataset
# -----------------------------
dataset = load_dataset("json", data_files=dataset_path, split="train")

def preprocess_function(examples):
    """
    For each row in the dataset, create the prompt by 
    substituting {issue} and {resolution} in the template.
    """
    # Make sure your dataset has "issue" and "resolution" fields
    texts = [
        prompt_template.format(issue=ex["issue"], resolution=ex["resolution"])
        for ex in examples
    ]
    return tokenizer(
        texts,
        padding="max_length",
        truncation=True,
        max_length=128
    )

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# -----------------------------
# Define Training Arguments
# -----------------------------
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,  # IMPORTANT: 'num_train_epochs', not 'num_train_epoch'
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=50,
    fp16=False,
    remove_unused_columns=False,
    # You can add more arguments as needed,
    # e.g., for evaluation, checkpointing, etc.
)

# -----------------------------
# Initialize Trainer
# -----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    # eval_dataset=...  # If you have a validation set, add here
)

# -----------------------------
# Fine-tune the model
# -----------------------------
print("Starting fine-tuning...")

# A simple way to check if we have any prior Trainer state:
resume_checkpoint = (
    os.path.exists(os.path.join(output_dir, "trainer_state.json"))
)

if resume_checkpoint:
    print("Resuming training from existing checkpoint...")
    trainer.train(resume_from_checkpoint=True)
else:
    print("No existing checkpoint found. Starting training from scratch...")
    trainer.train()

# -----------------------------
# Save the fine-tuned model
# -----------------------------
print("Saving the fine-tuned model to disk...")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"Model and tokenizer saved to: {output_dir}")

