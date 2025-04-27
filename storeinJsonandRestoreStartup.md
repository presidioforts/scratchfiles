### Minimal patch to add **disk persistence + startup restore + long “target” answers**  
(only the lines you need to insert or replace; leave everything else exactly as you have it.)

---

## 1 Imports (top of file)

```diff
-from torch.utils.data import DataLoader
-import pathlib, os, logging
+from torch.utils.data import DataLoader
+import pathlib, os, logging, json          # ← add json
```

---

## 2 Helpers & global state (just below `RUNS_DIR` definition)

```diff
+# ----------------------------------------------------------------------
+#  PERSISTENCE HELPERS  – newest pairs.json & load it
+# ----------------------------------------------------------------------
+def _latest_pairs_file() -> pathlib.Path | None:
+    files = sorted(
+        RUNS_DIR.glob("*/pairs.json"),
+        key=lambda p: p.parent.name,
+        reverse=True)
+    return files[0] if files else None
+
+def _load_pairs_from_disk() -> list["TrainingPair"]:
+    path = _latest_pairs_file()
+    if not path:
+        return []
+    with open(path, "r", encoding="utf-8") as f:
+        raw = json.load(f)
+    return [TrainingPair(**item) for item in raw]
+
+# in-memory store of all learned pairs (populated at startup)
+learned_pairs: list[TrainingPair] = _load_pairs_from_disk()
```

*(delete any previous `learned_pairs = []` you might have added earlier)*

---

## 3 Inside `fine_tune` – **save pairs & remember them**

```diff
     logger.info("[trainer] model.fit finished")
 
+    # ---- persist this run’s pairs & keep them in memory ---------------
+    with open(out_dir / "pairs.json", "w", encoding="utf-8") as f:
+        json.dump([p.model_dump() for p in pairs],
+                  f, ensure_ascii=False, indent=2)
+    learned_pairs.extend(pairs)
+    # ------------------------------------------------------------------
```

*(place this right after you create `out_dir` or before you reload the model; exact spot doesn’t matter)*

---

## 4 Replace body of `/troubleshoot` (keep header & try/except)

```diff
-        query_emb = model.encode(q.text, convert_to_tensor=True)
-        kb_embs   = model.encode(
-            [item["description"] for item in knowledge_base],
-            convert_to_tensor=True)
-        scores = util.cos_sim(query_emb, kb_embs)[0]
-        idx    = int(scores.argmax())
-
-        return {
-            "query": q.text,
-            "response": knowledge_base[idx]["resolution"],
-            "similarity_score": float(scores[idx]),
-        }
+        corpus_inputs  = [p.input  for p in learned_pairs] \
+                       + [item["description"] for item in knowledge_base]
+        corpus_answers = [p.target for p in learned_pairs] \
+                       + [item["resolution"]   for item in knowledge_base]
+
+        if not corpus_inputs:
+            raise ValueError("Search corpus is empty")
+
+        q_emb   = model.encode(q.text, convert_to_tensor=True)
+        c_emb   = model.encode(corpus_inputs, convert_to_tensor=True)
+        sims    = util.cos_sim(q_emb, c_emb)[0]
+        best    = int(sims.argmax())
+
+        return {
+            "query": q.text,
+            "response": corpus_answers[best],
+            "similarity_score": float(sims[best]),
+        }
```

---

### Done

* Pairs are dumped to `pairs.json` in every new `fine-tuned-YYYYMMDD-HHMMSS` folder.  
* On restart the app loads the newest file into memory.  
* `/troubleshoot` now searches both the learned pairs (full targets) and the original KB.

Nothing else in your file changes.  Apply, restart, and you’re running the next-level MVP.
