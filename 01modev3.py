
import os
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model

# =======================================
# CONFIG
# =======================================
local_model_path = "./llama-3.2-1b"   # Adjust to your local path
dataset_path = "issues_resolutions.json"
output_dir = "./finetuned_model"

# Prompt template
prompt_template = (
    "<|begin_of_text|><|start_header_id|>user<|end_header_id>\n"
    "Issue: {issue}\n"
    "Resolution: <|eot_id|><|start_header_id|>assistant<|end_header_id>\n"
    "{resolution}<|eot_id|>"
)

# =======================================
# LOAD DATASET & INSPECT
# =======================================
dataset = load_dataset("json", data_files=dataset_path, split="train")
print("Columns:", dataset.column_names)
print("First row:", dataset[0])  # Just to verify structure

# =======================================
# TOKENIZER & MODEL
# =======================================
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(local_model_path)

# Wrap model with LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # typical LLaMA QKV
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# =======================================
# PREPROCESS FUNCTION (NO 'labels' ADDED)
# =======================================
def preprocess_function(examples):
    issues = examples["issue"]
    resolutions = examples["resolution"]
    texts = []
    for issue_str, resolution_str in zip(issues, resolutions):
        text = prompt_template.format(issue=issue_str, resolution=resolution_str)
        texts.append(text)

    # Just tokenize; do not add labels
    return tokenizer(
        texts,
        padding="max_length",
        truncation=True,
        max_length=128
    )

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# =======================================
# USE DATA COLLATOR FOR CAUSAL LM
# =======================================
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, 
    mlm=False  # We want causal LM, not masked LM
)

# =======================================
# TRAINING ARGS
# =======================================
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=50,
    fp16=False,
    remove_unused_columns=False,
)

# =======================================
# TRAINER
# =======================================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    # This is where we add the collator
    data_collator=data_collator
)

trainer.train()

# =======================================
# SAVE
# =======================================
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
