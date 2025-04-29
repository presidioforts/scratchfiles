Perfect — thanks for clarifying.  
I'll adjust the article accordingly to reflect that **you stayed on Python 3.9** and **only fixed the packaging issue** (not Python upgrade).

Here's the corrected and final version for you to publish:

---

## 🛠️ Troubleshooting:  
**"NotImplementedError: Support for egg-based install has been removed"** during Python Build (Python 3.9 Environment)

---

### Problem
While building a Python project (running on Python 3.9), the build process failed with the following error:
```
NotImplementedError: Support for egg-based install has been removed
```
The error appeared when executing `python setup.py install`.

---

### Root Cause
- The project was using the **legacy `setup.py install` method**, which triggers **egg-based installation logic** (`do_egg_install`).
- Starting from **setuptools 66.0.0** (released January 2023), **egg-based installation was permanently removed**.
- Even though the Python version was still 3.9, the **`setuptools` package had upgraded**, causing the old build method to fail.

Reference: [Setuptools v66.0.0 Release Notes](https://setuptools.pypa.io/en/latest/history.html#v66-0-0)

---

### Solution
To fix the issue without changing the Python version:

1. **Removed** all uses of `python setup.py install` from build scripts and automation pipelines.
2. **Created a `pyproject.toml`** file in the project root to declare proper build requirements:
   
   ```toml
   [build-system]
   requires = [
       "setuptools==65.7.0",
       "wheel"
   ]
   build-backend = "setuptools.build_meta"
   ```

3. **Switched to modern install methods:**
   - Install directly:
     ```bash
     pip install .
     ```
   - Or build a wheel:
     ```bash
     python -m build
     pip install dist/*.whl
     ```

4. **Pinned `setuptools==65.7.0`** inside the project build system to ensure consistent behavior across environments.

---

✅ After these changes:
- Builds succeeded again without modifying the Python 3.9 runtime.
- Packaging and dependency management became compliant with modern Python standards (PEP 517/518).
- The system is now resilient to future `setuptools` upgrades.

---

Would you also like me to give you a **shorter "Executive Summary"** version if you plan to share this quickly by email too? (Optional) 🚀  
It'll be like a 5-line ultra-compact version.
