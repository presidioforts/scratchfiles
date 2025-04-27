# core ML stack ───────────────────────────────────────────────
numpy==1.26.4
torch==2.1.2+cpu             --index-url https://download.pytorch.org/whl/cpu
sentence-transformers==2.6.1

# API service ─────────────────────────────────────────────────
fastapi==0.110.1             # FastAPI 0.110+ uses Pydantic v2
uvicorn[standard]==0.28.0    # ASGI server

# UI client ──────────────────────────────────────────────────
streamlit==1.34.0
requests==2.31.0

# misc runtime helpers ───────────────────────────────────────
typing_extensions==4.10.0    # back-compat for some libs




# misc runtime helpers ───────────────────────────────────────

streamlit==1.34.0     # main UI framework
requests==2.31.0      # call the FastAPI backend

python -m venv venv-ui
venv-ui\Scripts\activate        # Linux/macOS: source venv-ui/bin/activate
pip install -r requirements-ui.txt


streamlit run ui_troubleshooter.py
