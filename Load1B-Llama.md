
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "path/to/my-llama-model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, 
                                             torch_dtype="float16",  # or as needed
                                             device_map="auto")      # or specify device

# Simple test
prompt = "Hello, how are you?"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
