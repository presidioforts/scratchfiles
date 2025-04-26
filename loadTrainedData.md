Below is the **smallest possible patch** to make `/troubleshoot` return the full *target* text you trained while leaving everything else untouched.

---

### 1  Add one global list (just below `knowledge_base`)

```diff
 knowledge_base: list[KnowledgeBaseItem] = [
     ...
 ]

+# remember every pair we fine-tune on (so /troubleshoot can use them)
+learned_pairs: list[TrainingPair] = []
```

---

### 2  Record the pairs when training finishes  
*(inside `fine_tune`, anywhere after `pairs` is validated but before you exit)*

```diff
     try:
         logger.info("[trainer] model.fit finished")
 
+        # ---- NEW ----------------------------------------------------
+        learned_pairs.extend(pairs)   # keep them for future similarity search
+        # -------------------------------------------------------------
```

*(position is flexible; it just needs to run once per training job)*

---

### 3  Replace the body of `/troubleshoot`  
*(delete the old lines and paste the few below)*

```diff
-        query_emb = model.encode(q.text, convert_to_tensor=True)
-        kb_embs   = model.encode(
-            [item["description"] for item in knowledge_base],
-            convert_to_tensor=True,
-        )
-        scores = util.cos_sim(query_emb, kb_embs)[0]
-        idx    = int(scores.argmax())
-
-        return {
-            "query": q.text,
-            "response": knowledge_base[idx]["resolution"],
-            "similarity_score": float(scores[idx]),
-        }
+        # build a single search corpus: learned inputs first, KB texts after
+        corpus_inputs  = [p.input for p in learned_pairs] \
+                       + [item["description"] for item in knowledge_base]
+        corpus_answers = [p.target for p in learned_pairs] \
+                       + [item["resolution"]   for item in knowledge_base]
+
+        if not corpus_inputs:
+            raise ValueError("Search corpus is empty")
+
+        query_emb  = model.encode(q.text, convert_to_tensor=True)
+        corp_embs  = model.encode(corpus_inputs, convert_to_tensor=True)
+        sims       = util.cos_sim(query_emb, corp_embs)[0]
+        best_idx   = int(sims.argmax())
+
+        return {
+            "query": q.text,
+            "response": corpus_answers[best_idx],
+            "similarity_score": float(sims[best_idx]),
+        }
```

---

**That’s it.**  
* One new global list  
* One line in `fine_tune`  
* A tiny replacement block in `/troubleshoot`

Now the endpoint will:

1. prefer resolutions from the pairs you fine-tuned on (full, detailed text)  
2. fall back to the original KB items if nothing else matches.
