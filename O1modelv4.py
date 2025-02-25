import os
import sys
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model

# ============================
# CONFIG
# ============================
local_model_path = "./llama-3.2-1b"   # <-- Put your local LLaMA or any GPT-like model here
dataset_path = "issues_resolutions.json"
output_dir = "./finetuned_model"

prompt_template = (
    "<|begin_of_text|><|start_header_id|>user<|end_header_id>\n"
    "Issue: {issue}\n"
    "Resolution: <|eot_id|><|start_header_id|>assistant<|end_header_id>\n"
    "{resolution}<|eot_id|>"
)

# ============================
# LOAD DATASET
# ============================
print("Loading dataset:", dataset_path)
dataset = load_dataset("json", data_files=dataset_path, split="train")

print("Columns:", dataset.column_names)
print("First row:", dataset[0])

# ============================
# TOKENIZER & MODEL
# ============================
print("Loading tokenizer & model from:", local_model_path)
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(local_model_path)

# Create LoRA config & wrap model
print("Wrapping model with LoRA...")
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # typical for LLaMA
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

# ============================
# PREPROCESS
# ============================
def preprocess_function(examples):
    # Combine "issue" + "resolution" into a single string prompt
    result_texts = []
    for issue_str, resolution_str in zip(examples["issue"], examples["resolution"]):
        text = prompt_template.format(issue=issue_str, resolution=resolution_str)
        result_texts.append(text)

    return tokenizer(
        result_texts,
        truncation=True,
        padding="max_length",
        max_length=128
    )

print("Tokenizing dataset...")
tokenized_dataset = dataset.map(preprocess_function, batched=True)
print("Sample tokenized row:", tokenized_dataset[0])

# ============================
# DATA COLLATOR
# ============================
print("Setting up DataCollatorForLanguageModeling...")
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # for causal LM
)

# ============================
# TRAINING ARGS
# ============================
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=1,
    num_train_epochs=1,
    logging_steps=1,
    save_steps=10,
    gradient_accumulation_steps=1,
    # You can switch to fp16=True if on GPU, etc.
    fp16=False,
    remove_unused_columns=False
)

# ============================
# TRAIN
# ============================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
)

print("Starting training...")
trainer.train()

# ============================
# SAVE
# ============================
print("Saving fine-tuned model & tokenizer to:", output_dir)
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print("Done.")
