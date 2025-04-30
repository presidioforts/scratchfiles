**DevOps Troubleshooting Guide**

**Error Message:**  
```
NotImplementedError: Support for egg-based install has been removed
```

---

## Problem

While building a Python project (using Python 3.9), the install step fails because the pipeline invokes:  
```bash
python setup.py install
```
Resulting in:
```
NotImplementedError: Support for egg-based install has been removed
```

---

## Root Cause

- The build script uses the **legacy** `python setup.py install` command.  
- As of **setuptools 66.0.0**, the internal egg-install logic was removed, so any call to it now raises `NotImplementedError`.  
- Although Python remained at 3.9, an upgrade of the project’s `setuptools` version broke the legacy install path.

---

## Solution

### ✅ Step 1: Remove Legacy Install Command

In all CI/CD scripts (e.g. `cicd.yml`), delete:
```diff
-    - run: python setup.py install
```

### ✅ Step 2: Add `pyproject.toml`

Create a `pyproject.toml` in your package root:

```toml
[build-system]
requires = [
  "setuptools>=42.0.0,<66.0.0",
  "wheel"
]
build-backend = "setuptools.build_meta"

[project]
name = "your-package-name"
dynamic = ["version"]
# … other project metadata …

[tool.setuptools]
packages = [
  "your_package1",
  "your_package2.subpkg",
  "your_package3"
]
# if your packages live under a non-standard directory, also specify:
# package-dir = { "" = "src" }
```

> • **Explicit packages list** avoids discovery and lists only known modules.  
> • **Version range** for `setuptools` prevents future forced downgrades.  
> • **Dependencies** remain managed separately (e.g., via `requirements.txt` or `[project].dependencies` if publishing).

### ✅ Step 3: Update Install Command

Replace any legacy install with a PEP 517-compliant pip install:

```diff
-    - run: python setup.py install
+    - run: pip install .
+    # or, for editable installs:
+    - run: pip install -e .
```

> **Note:** If your CI still uses `requirements.txt`, ensure it stays in sync with your package metadata.

---

## Behavior Before vs After

| With `setup.py install`         | With `pyproject.toml` & `pip install`      |
|---------------------------------|--------------------------------------------|
| Fails on setuptools ≥66         | Builds cleanly via PEP 517 wheel backend    |
| Relies on removed egg logic     | Uses isolated wheel build and metadata      |

---

## Summary

- **Remove** all `python setup.py install` calls.  
- **Introduce** `pyproject.toml` with explicit package listings under `[tool.setuptools]`.  
- **Switch** install commands to `pip install .` (or `-e .`).  
- **Pin** `setuptools>=42.0.0,<66.0.0` to avoid egg-install removals.  
- **Sync** any `requirements.txt` if still in use for dependencies.

---

## Final Build Result ✅

- Builds succeed under current and future setuptools versions.  
- Artifacts include correct metadata for PyPI/Artifactory.  
- CI/CD pipelines require no further changes beyond the above.

---

## References

- [Setuptools 66.0.0 Release Notes](https://setuptools.pypa.io/en/latest/history.html#v66-0-0)  
- [PEP 517 – A Build-System Independent Format](https://peps.python.org/pep-0517/)  
- [PEP 621 – Standardizing Project Metadata](https://peps.python.org/pep-0621/)
