# ---------- Build stage ----------
    FROM python:3.11-slim

    # Keep the HF model cache so Cloud Run can reuse it between cold starts
    ENV HUGGINGFACE_HUB_CACHE=/models \
        PYTHONUNBUFFERED=1
    
    WORKDIR /app
    
    # Install dependencies
    RUN pip install --no-cache-dir \
            sentence-transformers==2.6.1 \
            fastapi uvicorn[standard] torch
    
    # Copy source
    COPY app.py .
    
    # Expose default port
    EXPOSE 8080
    
    # Entrypoint
    CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
    
