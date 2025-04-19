
import streamlit as st
import difflib
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)
from pathlib import Path

# --- Model Location (local only) ---
MODEL_ID = "../Phi-3.5-mini-instruct"  # Adjust this if your path is different

# --- Load Tokenizer & Model from local folder ---
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(MODEL_ID, local_files_only=True)

# --- Create Text Generation Pipeline ---
generator = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer
)

# --- Streamlit UI ---
st.set_page_config(page_title="Grammar Correction (Phi 3.5 Mini)", layout="centered")
st.title("Grammar Correction Tool (Offline, Local Model)")

input_text = st.text_area("Enter your text:", height=200)
corrected_text = ""

if st.button("Correct Grammar") and input_text.strip():
    prompt = f"Correct the grammar and rewrite professionally:\n{input_text.strip()}"
    with st.spinner("Correcting..."):
        output = generator(prompt, max_new_tokens=200, temperature=0.7)[0]["generated_text"]
        corrected_text = output.replace(prompt, "").strip()

    st.subheader("Corrected Text:")
    st.write(corrected_text)

    # Show word-level diff
    st.subheader("Changes Highlight:")
    diff = difflib.ndiff(input_text.split(), corrected_text.split())
    diff_marked = [
        f"**:green[{w[2:]}]**" if w.startswith('+ ')
        else f"**:red[{w[2:]}]**" if w.startswith('- ')
        else w[2:]
        for w in diff
    ]
    st.markdown(" ".join(diff_marked))

    # Download option
    st.download_button("Download Corrected Text", corrected_text, file_name="corrected_text.txt")

# --- Model Health Debug (Optional) ---
with st.expander("Debug Info"):
    st.write("Model Path:", MODEL_ID)
    st.write("Model folder contents:", list(Path(MODEL_ID).glob("*")))
    st.write("Transformers version check:")
    import transformers
    st.code(transformers.__version__)
    st.write("Model config rope_scaling:")
    st.json(model.config.to_dict().get("rope_scaling", "Not defined"))

st.markdown("---")
st.caption("Running on CPU | Local Model | Phi-3.5-mini-instruct")
