
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model
import os

# Path to your local model, dataset, etc.
local_model_path = "./llama-3.2-1b"
dataset_path = "issues_resolutions.json"
output_dir = "./finetuned_model"

# A sample prompt template
prompt_template = (
    "<|begin_of_text|><|start_header_id|>user<|end_header_id>\n"
    "Issue: {issue}\n"
    "Resolution: <|eot_id|><|start_header_id|>assistant<|end_header_id>\n"
    "{resolution}<|eot_id|>"
)

# 1) Load dataset
dataset = load_dataset("json", data_files=dataset_path, split="train")
print("Columns:", dataset.column_names)  # should be ['issue', 'resolution']
print("First row:", dataset[0])

# 2) Define the preprocess function (note the use of zip)
def preprocess_function(examples):
    """
    examples["issue"] is a list of strings (batched). 
    examples["resolution"] is also a list of strings.
    We zip them so we can build each prompt properly.
    """
    issues = examples["issue"]
    resolutions = examples["resolution"]

    prompts = []
    for issue_str, resolution_str in zip(issues, resolutions):
        text = prompt_template.format(issue=issue_str, resolution=resolution_str)
        prompts.append(text)

    # Then tokenize
    return tokenizer(
        prompts,
        padding="max_length",
        truncation=True,
        max_length=128
    )

# 3) Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
# If needed, set pad token to eos token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(local_model_path)

# 4) Wrap the base model with LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # typical for LLaMA
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# 5) Tokenize entire dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# 6) Define training arguments
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=1,  # use 1 for quick testing
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=50,
    fp16=False,
    remove_unused_columns=False
)

# 7) Initialize Trainer and train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

# 8) Save the final model & tokenizer
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
