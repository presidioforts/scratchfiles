Here's an **inference script** to test your fine-tuned LLaMA 3.2 Instruct 1B model with LoRA.

---

## **🔹 Inference Script for Fine-Tuned LLaMA Model**
This script:
✔ Loads the **fine-tuned model** from `batch_finetuned_llama`  
✔ Accepts **user queries** (issues)  
✔ Generates **resolutions** based on fine-tuned knowledge  
✔ Runs inference on **CPU or GPU** automatically  

---

### **📜 `run_inference.py`**
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# -------------------------------------------------------------------
# 1) CONFIGURATION
# -------------------------------------------------------------------
MODEL_PATH = "./batch_finetuned_llama"  # Update if needed
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------------------------------------------------------------------
# 2) LOAD MODEL & TOKENIZER
# -------------------------------------------------------------------
print(f">>> Loading tokenizer from: {MODEL_PATH}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print(f">>> Loading fine-tuned model from: {MODEL_PATH}")
base_model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
model = PeftModel.from_pretrained(base_model, MODEL_PATH)

model.to(DEVICE)
model.eval()

# -------------------------------------------------------------------
# 3) GENERATION FUNCTION
# -------------------------------------------------------------------
def generate_resolution(issue_text, max_tokens=150):
    """
    Generates a resolution for a given issue using the fine-tuned model.
    """
    prompt = f"<|begin_of_text|>\nIssue: {issue_text}\nResolution:"
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=max_tokens,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response.split("Resolution:")[-1].strip()  # Extract resolution


# -------------------------------------------------------------------
# 4) RUN INFERENCE (INTERACTIVE)
# -------------------------------------------------------------------
print("\n>>> DevOps AI Assistant Ready! Type 'exit' to quit.")
while True:
    user_input = input("\nEnter an issue: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    resolution = generate_resolution(user_input)
    print(f"\n💡 Suggested Resolution: {resolution}")
```

---

## **🔹 How to Run the Script**
1️⃣ **Save this script** as `run_inference.py`  
2️⃣ **Run in terminal**:
   ```bash
   python run_inference.py
   ```
3️⃣ **Type an issue** (e.g., "Build failed due to missing dependency.")  
4️⃣ **Get a resolution** 🎯  

---

## **🔹 Expected Output Example**
```
>>> DevOps AI Assistant Ready! Type 'exit' to quit.

Enter an issue: Deployment stuck in pending state.

💡 Suggested Resolution: Increase the CI/CD timeout or check container logs.
```

---

## **🔹 Next Steps**
✅ **Test inference** with real issues  
✅ **Deploy as API** using **FastAPI**  
✅ **Optimize responses** (if needed, tweak prompt formatting)  

Would you like an API version using **FastAPI** for integration? 🚀
