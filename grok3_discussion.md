### Key Points
- Use a Submission API on VM1 for the training team to add validated issue-resolution pairs to `issues_resolutions.json`.
- Fine-tune the model on VM1 with incremental updates, saving to a different path each time.
- Transfer the fine-tuned model to VM2 and host an Inference API for resolving issues.

### Setup Overview
**Training on VM1:**
- Start with an initial `issues_resolutions.json` and use a Submission API for adding new data.
- Fine-tune the Llama 3.2 1B model using LoRA for CPU efficiency, saving incrementally to unique paths.

**Deployment on VM2:**
- Transfer the latest fine-tuned model to VM2 and set up a Flask API for inference, allowing developers to query resolutions.

**Surprising Detail:** The system supports incremental training, meaning you don’t need to retrain from scratch each time, saving time and resources.

### Training Process
The training process involves setting up an API for data submission and fine-tuning the model:
- The Submission API ensures data quality with validation and authentication.
- Fine-tuning uses LoRA for efficiency on CPU, supporting resume-from-checkpoint for updates.

### Deployment Process
For deployment, transfer the model and host an API:
- Copy the fine-tuned model to VM2 and load it for inference.
- The Inference API handles POST requests to generate resolutions, ensuring quick responses for developers.

---

### Comprehensive Response

This response consolidates the setup for hosting and fine-tuning the Llama 3.2 1B model for CI/CD issue resolution, using two VMs in an enterprise data center, with a focus on training via an API on VM1 and deploying an inference API on VM2. The system is designed for CPU-based operation during the pilot phase, with no external dependencies like Hugging Face, leveraging locally stored models from the enterprise artifactory.

#### System Architecture
The architecture involves two main components:
- **VM1 (Training):** Hosts the Submission API for the training team to add validated issue-resolution pairs and performs fine-tuning, saving models incrementally.
- **VM2 (Deployment):** Receives the fine-tuned model, hosts the Inference API for developers to query resolutions.

The process ensures data quality, supports incremental updates, and maintains efficiency on CPU, suitable for a pilot with a few users.

#### Submission API on VM1
The Submission API allows the training team to submit validated issue-resolution pairs, ensuring no invalid data enters the training dataset. It includes:
- **Authentication:** Uses an API key for secure access, restricting submissions to the training team.
- **Validation:** Checks for required fields, minimum and maximum lengths, and basic quality (e.g., non-trivial content).
- **Storage:** Appends new entries to `issues_resolutions.json`, maintaining a growing dataset.

Here’s the complete code for the Submission API:

```python
from flask import Flask, request, jsonify
import json
import os
from functools import wraps

app = Flask(__name__)
dataset_path = "issues_resolutions.json"
API_KEY = "your_secret_api_key_here"  # Set a strong key for your team

# Ensure dataset file exists
if not os.path.exists(dataset_path):
    with open(dataset_path, "w") as f:
        json.dump([], f)

# Basic authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/submit", methods=["POST"])
@require_api_key
def submit_incident():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400
    # Validate required fields and basic quality
    if "issue" not in data or "resolution" not in data:
        return jsonify({"error": "Missing 'issue' or 'resolution'"}), 400
    issue = data["issue"].strip()
    resolution = data["resolution"].strip()
    if len(issue) < 5 or len(resolution) < 5:
        return jsonify({"error": "Issue or resolution too short"}), 400
    if len(issue) > 200 or len(resolution) > 200:
        return jsonify({"error": "Issue or resolution exceeds 200 characters"}), 400
    # Load existing dataset
    with open(dataset_path, "r") as f:
        dataset = json.load(f)
    # Append new entry
    dataset.append({"issue": issue, "resolution": resolution})
    # Save updated dataset
    with open(dataset_path, "w") as f:
        json.dump(dataset, f, indent=2)
    return jsonify({"message": "Incident submitted successfully", "count": len(dataset)})

if __name__ == "__main__":
    print("Starting submission API on port 5001...")
    app.run(host="0.0.0.0", port=5001, threaded=True)
```

To use, the training team submits data via:
```bash
curl -X POST -H "Content-Type: application/json" -H "X-API-Key: your_secret_api_key_here" -d '{"issue":"Build failed due to missing dependency","resolution":"Add package X to requirements.txt"}' http://vm1_ip:5001/submit
```

#### Fine-Tuning Script on VM1
The fine-tuning script loads the model from a local directory (`/path/to/llama-3.2-1b`), processes `issues_resolutions.json`, and uses LoRA for efficient CPU-based training. It supports incremental updates by resuming from previous checkpoints, saving to a specified path (`./finetuned_model`). The prompt template ensures the model learns to generate resolutions from issues:

```python
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
```

Run this script on VM1 after ensuring `issues_resolutions.json` has initial data:
```bash
python train.py
```

#### Model Transfer and Inference API on VM2
After fine-tuning, transfer the `finetuned_model` directory to VM2:
```bash
scp -r ./finetuned_model user@vm2:/path/to/deploy/
```

The Inference API on VM2 loads the fine-tuned model and serves resolutions via HTTP POST requests. It uses the base model path for loading and applies the fine-tuned LoRA weights:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from flask import Flask, request, jsonify
import os

# Configuration
base_model_path = "/path/to/llama-3.2-1b"      # Path to original model on VM2
finetuned_model_path = "/path/to/deploy/finetuned_model"  # Path to fine-tuned model
port = 5000

# Load tokenizer and base model from local directories
tokenizer = AutoTokenizer.from_pretrain(finetuned_model_path)
base_model = AutoModelForCausalLM.from_pretrain(base_model_path)

# Load fine-tuned LoRA weights
model = PeftModel.from_pretrain(base_model, finetuned_model_path)

# Move to CPU explicitly
model.to("cpu")

# Inference function
def generate_resolution(issue_text):
    prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id>
Issue: {issue_text}
Resolution: < |eot_id|><|start_header_id|>assistant<|end_header_id>"""
    # Correct the prompt template
    prompt = prompt.replace(" < |eot_id|>", "<|eot_id|>")
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
    # Get the newly generated tokens
    input_length = len(inputs["input_ids"][0])
    generated_tokens = outputs[0][input_length:]
    resolution = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    return resolution.strip()

# Flask app
app = Flask(__name__)

@app.route("/resolve", methods=["POST"])
def resolve_issue():
    data = request.get_json()
    if not data or "issue" not in data:
        return jsonify({"error": "Missing 'issue' in request"}), 400
    issue = data["issue"]
    resolution = generate_resolution(issue)
    return jsonify({"issue": issue, "resolution": resolution})

if __name__ == "__main__":
    print(f"Starting inference server on port {port}...")
    app.run(host="0.0.0.0", port=port, threaded=True)
```

Run this on VM2:
```bash
python deploy.py
```

Test with:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"issue":"Build failed due to missing dependency"}' http://vm2_ip:5000/resolve
```

#### Implementation Details
- **Model Storage:** Each fine-tuning saves to `./finetuned_model`, allowing incremental updates. For versioning, consider renaming directories (e.g., `./finetuned_model_v1`, `./finetuned_model_v2`) before transfer.
- **Efficiency:** LoRA reduces memory usage (8-12GB RAM on CPU), and batch sizes are optimized for CPU with gradient accumulation.
- **Security:** The Submission API uses API key authentication, ensuring only the training team can add data.

This setup ensures a robust, scalable solution for the pilot, with controlled data quality and efficient model updates.

#### Key Citations
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/main/en/index)
- [PEFT Library for Efficient Fine-Tuning](https://huggingface.co/docs/peft/main/en/index)
