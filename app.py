from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, InputExample, losses, util
from torch.utils.data import DataLoader
import pathlib, os, torch
import logging

# ----------------------------------------------------------------------
# Globals
# ----------------------------------------------------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CACHE_DIR = os.getenv("HUGGINGFACE_HUB_CACHE", "/models")
MODEL_PATH = pathlib.Path(CACHE_DIR) / "fine-tuned"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the base (or previously fine-tuned) model at startup
try:
    model = SentenceTransformer(
        MODEL_PATH if MODEL_PATH.exists() else MODEL_NAME
    )
    # Check if the model loaded correctly (optional)
    test_embedding = model.encode("test")
    logger.info(f"Model loaded successfully from: {MODEL_PATH if MODEL_PATH.exists() else MODEL_NAME}, shape: {test_embedding.shape}")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    # It's crucial to handle this error, you might want to raise an exception to prevent the app from starting
    raise  # Re-raise the exception so that the app doesn't start.

# ----------------------------------------------------------------------
# FastAPI setup
# ----------------------------------------------------------------------
app = FastAPI()


class Query(BaseModel):
    text: str


class TrainingPair(BaseModel):
    input: str
    target: str


class TrainingData(BaseModel):
    data: list[TrainingPair]


class KnowledgeBaseItem(BaseModel):
    description: str
    resolution: str


# In-memory KB for MVP (replace with DB later)
knowledge_base: list[KnowledgeBaseItem] = [
    {
        "description": "npm ERR! code ERESOLVE",
        "resolution": "Delete node_modules & package-lock.json, then run npm install.",
    },
    {
        "description": "Script not running after package install",
        "resolution": "Check package.json scripts and dependencies.",
    },
    {
        "description": "npm install hangs",
        "resolution": "Clear npm cache (`npm cache clean --force`) or check network.",
    },
    {
        "description": "Update npm version",
        "resolution": "Run `npm install -g npm@latest`.",
    },
]


# ----------------------------------------------------------------------
# Background fine-tune worker
# ----------------------------------------------------------------------
def fine_tune(pairs: list[TrainingPair]):
    global model
    logger.info(f"[trainer] starting fine-tune with {len(pairs)} pairs")

    try:
        examples = [InputExample(texts=[p.input, p.target]) for p in pairs]
        loader = DataLoader(examples, shuffle=True, batch_size=8)
        loss_fn = losses.CosineSimilarityLoss(model)

        logger.info("[trainer] starting model.fit")  # Add start log
        # Use a smaller number of epochs for the MVP
        model.fit(
            train_objectives=[(loader, loss_fn)],
            epochs=1,
            optimizer_params={"lr": 1e-5},
            show_progress_bar=False,  # Good to disable in Cloud Run
        )
        logger.info("[trainer] model.fit complete")  # Add end log

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        model.save(str(MODEL_PATH))
        logger.info(f"[trainer] fine-tune finished – model saved to {MODEL_PATH}")

        # Reload in-memory copy so new weights serve future requests
        model = SentenceTransformer(str(MODEL_PATH))
        logger.info("[trainer] model reloaded for inference")

    except Exception as e:
        logger.error(f"[trainer] ERROR: fine-tuning failed: {e}")  # Log the error
        #  Important:  Consider how to handle this error.
        #  In a production system, you might want to:
        #  1.  Retry the training
        #  2.  Send an alert to an administrator
        #  3.  Store the error in a database
        #  For this MVP, we will just log and exit.
        return  # Exit the function

# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------
@app.post("/train")
async def train_model(payload: TrainingData, bg: BackgroundTasks):
    """
    Accepts training pairs and kicks off a background fine-tune.
    Quickly returns so the caller isn’t kept waiting.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="No training data received.")

    # Launch trainer in the background
    bg.add_task(fine_tune, payload.data)
    return {"message": f"Training job started with {len(payload.data)} pairs."}


@app.post("/troubleshoot")
async def troubleshoot(q: Query):
    """
    Returns the KB resolution whose description best matches the query.
    """
    try:
        query_emb = model.encode(q.text, convert_to_tensor=True)
        kb_embs = model.encode(
            [item["description"] for item in knowledge_base],
            convert_to_tensor=True,
        )
        scores = util.cos_sim(query_emb, kb_embs)[0]
        idx = int(scores.argmax())
        return {
            "query": q.text,
            "response": knowledge_base[idx]["resolution"],
            "similarity_score": float(scores[idx]),
        }
    except Exception as e:
        logger.error(f"Error in /troubleshoot: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred during troubleshooting."
        )

# Optional – makes `python app.py` work for local testing
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8080)
