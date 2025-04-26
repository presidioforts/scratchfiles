Below is a **minimal patch** that adds the “one-folder-per-run” feature to the code you just sent.  
Apply these edits (≈ 35 lines) and nothing else changes.

---

### 1 . Globals – new `RUNS_DIR`

```diff
-BASE_MODEL_DIR   = LOCAL_MODELS_DIR / "all-MiniLM-L6-v2"   # has config.json, tokenizer.json …
-FINETUNED_DIR    = BASE_MODEL_DIR  / "fine-tuned"          # our fine-tuned weights will live here
+# base model location
+BASE_MODEL_DIR   = LOCAL_MODELS_DIR / "all-MiniLM-L6-v2"
+
+# NEW: every fine-tune run is saved to its own timestamped folder
+RUNS_DIR         = BASE_MODEL_DIR / "fine-tuned-runs"
+RUNS_DIR.mkdir(parents=True, exist_ok=True)
+
+# (optional backward-compat) legacy single folder, if you already have one
+LEGACY_DIR       = BASE_MODEL_DIR / "fine-tuned"
```

---

### 2 . Helpers – latest & new run directories

```diff
@@
 logger = logging.getLogger(__name__)
 
+# ----------------------------------------------------------------------
+# Helpers for run directories
+# ----------------------------------------------------------------------
+from datetime import datetime
+
+def _latest_run_dir() -> pathlib.Path | None:
+    """Return newest timestamped run dir, else legacy dir, else None."""
+    runs = sorted((p for p in RUNS_DIR.iterdir() if p.is_dir()),
+                  key=lambda p: p.name,
+                  reverse=True)
+    return runs[0] if runs else (LEGACY_DIR if LEGACY_DIR.exists() else None)
+
+def _new_run_dir() -> pathlib.Path:
+    ts  = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
+    out = RUNS_DIR / f"fine-tuned-{ts}"
+    out.mkdir(parents=True, exist_ok=False)
+    return out
```

---

### 3 . Model load at startup

```diff
-    load_path = FINETUNED_DIR if FINETUNED_DIR.exists() else BASE_MODEL_DIR
+    load_path = _latest_run_dir() or BASE_MODEL_DIR
```

---

### 4 . Save & reload inside `fine_tune`

```diff
-        # ensure directory exists and save new weights
-        FINETUNED_DIR.mkdir(parents=True, exist_ok=True)
-        model.save(str(FINETUNED_DIR))
-        logger.info("[trainer] saved fine-tuned model to %s", FINETUNED_DIR)
-
-        # hot-reload the updated model for immediate inference
-        model = SentenceTransformer(str(FINETUNED_DIR))
-        logger.info("[trainer] reloaded fine-tuned model")
+        out_dir = _new_run_dir()
+        model.save(str(out_dir))
+        logger.info("[trainer] saved fine-tuned model to %s", out_dir)
+
+        # hot-reload the updated model
+        model = SentenceTransformer(str(out_dir))
+        logger.info("[trainer] reloaded fine-tuned model")
```

*(indentation in the rest of `fine_tune` stays the same; only the block above changes)*

---

That’s it—each training job now lands in its own folder:

```
C:\models\all-MiniLM-L6-v2\fine-tuned-runs\
    └─ fine-tuned-20250426-170212\
    └─ fine-tuned-20250426-171045\
    └─ …
```

On startup the service automatically picks the **most-recent** run; if none exist it still falls back to the base model.

No other behaviour or API signature changed, so your diff remains small and review-friendly.
