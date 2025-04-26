"""
Updated FastAPI service
- Loads Sentence-Transformer **exclusively from the local filesystem**
  (no Hugging Face Hub calls, completely offline).
- Fine-tuned weights are saved to and re-loaded from
  C:\models\all-MiniLM-L6-v2\fine-tuned
Everything else (API routes, training loop, KB, etc.) is unchanged.
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, InputExample, losses, util
from torch.utils.data import DataLoader
import pathlib, os, logging

# ----------------------------------------------------------------------
# Globals – LOCAL-ONLY MODEL SETUP
# ----------------------------------------------------------------------
# 1️⃣  Point to the directory where the base model is stored
LOCAL_MODELS_DIR = pathlib.Path(r"C:\models")
BASE_MODEL_DIR   = LOCAL_MODELS_DIR / "all-MiniLM-L6-v2"   # has config.json, tokenizer.json …
FINETUNED_DIR    = BASE_MODEL_DIR  / "fine-tuned"          # our fine-tuned weights will live here

# 2️⃣  Guarantee offline mode for the HF backend libraries
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_OFFLINE"]               = "1"

# 3️⃣  Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 4️⃣  Load either fine-tuned model (if present) or the base model
try:
    load_path = FINETUNED_DIR if FINETUNED_DIR.exists() else BASE_MODEL_DIR
    model = SentenceTransformer(str(load_path))

    # quick health-check
    _ = model.encode("health-check")
    logger.info("✅  Model loaded from %s", load_path)

except Exception as e:
    logger.error("❌  Failed to load model: %s", e)
    raise  # abort app start-up if model can’t be loaded

# ----------------------------------------------------------------------
# FastAPI setup
# ----------------------------------------------------------------------
app = FastAPI()

# ----------------------------- Data Models ----------------------------
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


# --------------------------- In-memory KB -----------------------------
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
# Background fine-tuning worker
# ----------------------------------------------------------------------
def fine_tune(pairs: list[TrainingPair]) -> None:
    """
    Runs in a background thread; fine-tunes the sentence-transformer on
    the provided input/target pairs, then saves & hot-reloads the weights.
    """
    global model
    logger.info("[trainer] starting fine-tune with %d pairs", len(pairs))

    try:
        examples = [InputExample(texts=[p.input, p.target]) for p in pairs]
        loader   = DataLoader(examples, shuffle=True, batch_size=8)
        loss_fn  = losses.CosineSimilarityLoss(model)

        logger.info("[trainer] model.fit starting")
        model.fit(
            train_objectives=[(loader, loss_fn)],
            epochs=1,                    # light MVP training
            optimizer_params={"lr": 1e-5},
            show_progress_bar=False,
        )
        logger.info("[trainer] model.fit finished")

        # ensure directory exists and save new weights
        FINETUNED_DIR.mkdir(parents=True, exist_ok=True)
        model.save(str(FINETUNED_DIR))
        logger.info("[trainer] saved fine-tuned model to %s", FINETUNED_DIR)

        # hot-reload the updated model for immediate inference
        model = SentenceTransformer(str(FINETUNED_DIR))
        logger.info("[trainer] reloaded fine-tuned model")

    except Exception as e:
        logger.error("[trainer] training failed: %s", e)
        # Decide how to handle (alert, retry, etc.); for MVP we just log.
        return

# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------
@app.post("/train")
async def train_model(payload: TrainingData, bg: BackgroundTasks):
    """
    Kick off background fine-tuning with the supplied pairs.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="No training data received.")

    bg.add_task(fine_tune, payload.data)
    return {"message": f"Training job started with {len(payload.data)} pairs."}


@app.post("/troubleshoot")
async def troubleshoot(q: Query):
    """
    Find the KB resolution whose description is most similar to the query.
    """
    try:
        query_emb = model.encode(q.text, convert_to_tensor=True)
        kb_embs   = model.encode(
            [item["description"] for item in knowledge_base],
            convert_to_tensor=True,
        )
        scores = util.cos_sim(query_emb, kb_embs)[0]
        idx    = int(scores.argmax())

        return {
            "query": q.text,
            "response": knowledge_base[idx]["resolution"],
            "similarity_score": float(scores[idx]),
        }

    except Exception as e:
        logger.error("Error in /troubleshoot: %s", e)
        raise HTTPException(status_code=500, detail="An error occurred during troubleshooting.")

# ----------------------------------------------------------------------
# Local dev entry-point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080)
