import streamlit as st
import difflib
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
)

MODEL_ID = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(MODEL_ID, local_files_only=True)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Grammar Corrector (Phi‑3 Mini)", layout="centered")
st.title("Grammar Correction Tool")

input_text = st.text_area("Enter your text:", height=200)

if st.button("Correct Grammar") and input_text.strip():
    if len(input_text) > 4_000:
        st.warning("Text too long—please paste ≤ 4 000 characters.")
        st.stop()

    prompt = f"Correct the grammar and rewrite professionally:\n{input_text.strip()}"
    with st.spinner("Correcting…"):
        result = generator(prompt, max_new_tokens=200, temperature=0.7)[0]["generated_text"]
        corrected = result.replace(prompt, "").strip()

    st.subheader("Corrected Text:")
    st.write(corrected)

    st.subheader("Changes Highlight:")
    diff = difflib.ndiff(input_text.split(), corrected.split())
    st.markdown(
        " ".join(
            f"**:green[{w[2:]}]**" if w.startswith("+ ")
            else f"**:red[{w[2:]}]**" if w.startswith("- ")
            else w[2:]
            for w in diff
        )
    )

    st.download_button("Download Corrected Text", corrected, file_name="corrected_text.txt")

st.markdown("---")
st.caption("Powered by Phi‑3‑mini‑instruct (offline, CPU)")
