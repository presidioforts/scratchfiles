@@
-CACHE_DIR      = pathlib.Path(os.getenv("HUGGINGFACE_HUB_CACHE", "/models"))
-MODEL_PATH     = pathlib.Path(CACHE_DIR) / "fine-tuned"
+# cache root
+CACHE_DIR = pathlib.Path(os.getenv("HUGGINGFACE_HUB_CACHE", "/models"))
+
+# every fine-tune run will be saved under   …/fine-tuned-runs/fine-tuned-YYYYMMDD-HHMMSS
+RUNS_DIR  = CACHE_DIR / "fine-tuned-runs"
+RUNS_DIR.mkdir(parents=True, exist_ok=True)
+
+# ----------------------------------------------------------------------
+# helpers for latest + new run dirs
+# ----------------------------------------------------------------------
+def _latest_run_dir() -> pathlib.Path | None:
+    runs = sorted((p for p in RUNS_DIR.iterdir() if p.is_dir()),
+                  key=lambda p: p.name,
+                  reverse=True)
+    return runs[0] if runs else None
+
+def _new_run_dir() -> pathlib.Path:
+    ts  = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
+    out = RUNS_DIR / f"fine-tuned-{ts}"
+    out.mkdir(parents=True, exist_ok=False)
+    return out
diff
Copy
Edit
-# Model load at startup
-# ----------------------------------------------------------------------
-try:
-    load_path = latest_run_dir()
-    model = SentenceTransformer(str(load_path)) if load_path else SentenceTransformer(MODEL_NAME)
-    logger.info(f"Model loaded from: {load_path if load_path else MODEL_NAME}")
+# Model load at startup
+# ----------------------------------------------------------------------
+try:
+    load_path = _latest_run_dir()
+    model = SentenceTransformer(str(load_path)) if load_path else SentenceTransformer(MODEL_NAME)
+    logger.info(f"Model loaded from: {load_path if load_path else MODEL_NAME}")
@@
-        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
-        model.save(str(MODEL_PATH))
-        logger.info(f"[trainer] fine-tune finished – model saved to {MODEL_PATH}")
-
-        # Reload in-memory copy so new weights serve future requests
-        model = SentenceTransformer(str(MODEL_PATH))
+        out_dir = _new_run_dir()
+        model.save(str(out_dir))
+        logger.info(f"[trainer] fine-tune finished – model saved to {out_dir}")
+
+        # reload latest weights for inference
+        model = SentenceTransformer(str(out_dir))
