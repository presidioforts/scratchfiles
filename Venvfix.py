
python - <<'PY'
import sys, site, pkg_resources as p, os
print("User‑site enabled: ", site.ENABLE_USER_SITE)
print("Env var PYTHONNOUSERSITE:", os.getenv("PYTHONNOUSERSITE"))

print("\nAny paths from AppData\\Roaming?")
roaming = [p for p in sys.path if "AppData" in p]
print(roaming or "None")

print("\nKey package versions:")
for name in ("transformers", "huggingface_hub", "torch", "streamlit"):
    try:
        print(f"  {name:<17} {p.get_distribution(name).version}")
    except p.DistributionNotFound:
        print(f"  {name:<17} (not installed)")
PY
