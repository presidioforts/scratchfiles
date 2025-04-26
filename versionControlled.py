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
