Below is an example `requirements.txt` that should cover all the major libraries used in the script. These versions are typical at the time of writing; you can adjust them as needed based on your environment or preference.

```txt
numpy==1.23.5
faiss-cpu==1.7.3
pdfplumber==0.9.0
nltk==3.7
sentence-transformers==2.2.2
```

**Notes**:
1. If you have a GPU and want GPU acceleration for Faiss, use `faiss-gpu` instead of `faiss-cpu`.
2. These pinned versions are just an example. You can remove version pins (the `==`) if you prefer the latest versions or have compatibility constraints with other packages.  
3. You may also want to ensure `transformers` is installed, which is typically included as a dependency of `sentence-transformers`. If needed, add it explicitly:
   ```txt
   transformers==4.26.1
   ```
