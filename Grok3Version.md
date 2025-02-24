import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, PeftModel
import os

# Configuration
local_model_path = "/path/to/llama-3.2-1b"     # Path to the model directory on VM1
dataset_path = "issues_resolutions.json"       # Your dataset
output_dir = "./finetuned_model"               # Where to save the fine-tuned model

# Prompt template for Llama 3.2
prompt_template = """<|begin_of_text|><|start_header_id|>user<|end_header_id>
Issue: {issue}
Resolution: < |eot_id|><|start_header_id|>assistant<|end_header_id>
{resolution}<|eot_id|>"""

# Load tokenizer and model from local directory
tokenizer = AutoTokenizer.from_pretrain(local_model_path)
if os.path.exists(output_dir):
    # Load the previous fine-tuned model
    base_model = AutoModelForCausalLM.from_pretrain(local_model_path)
    model = PeftModel.from_pretrain(base_model, output_dir)
else:
    model = AutoModelForCausalLM.from_pretrain(local_model_path)
    # Configure LoRA for efficient fine-tuning
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

# Set padding token (if not set)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load and prepare dataset
dataset = load_dataset("json", data_files=dataset_path, split="train")

def preprocess_function(examples):
    texts = [prompt_template.format(issue=ex["issue"], resolution=ex["resolution"]) for ex in examples]
    return tokenizer(texts, padding="max_length", truncation=True, max_length=128)

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Training arguments (CPU-friendly)
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epoch=3,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=50,
    fp16=False,
    remove_unused_columns=False
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Fine-tune the model
print("Starting fine-tuning...")
if os.path.exists(output_dir):
    # Resume from checkpoint
    trainer.train(resume_from_checkpoint=True)
else:
    trainer.train()

# Save the fine-tuned model and tokenizer
print("Saving fine-tuned model...")
model.save_pretrain(output_dir)
tokenizer.save_pretrain(output_dir)
print(f"Model saved to {output_dir}")
