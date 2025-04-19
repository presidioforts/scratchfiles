
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_ID = r"C:\Users\u425154\2025-AI-WorkSpace\docEx\Phi-3.5-mini-instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(MODEL_ID, local_files_only=True)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt = "Correct the grammar and rewrite professionally:\nShe don’t has no idea how does the system works."

output = generator(prompt, max_new_tokens=64, temperature=0.7)[0]["generated_text"]
corrected = output.replace(prompt, "").strip()

print("\nCorrected Text:")
print(corrected)
