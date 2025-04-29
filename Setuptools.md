[build-system]
requires = ["setuptools==65.7.0", "wheel"]
build-backend = "setuptools.build_meta"





You're right:

The build step logs show that pip3 install is being run without a setuptools version constraint.

As a result, it installs setuptools 58.1.0, which still has egg support partially broken and breaks setup.py install.



---

Fix Strategy 1: Force it via pyproject.toml

Yes — the modern way to enforce build-time dependencies is with a pyproject.toml. Here's how:

pyproject.toml (to be added in your repo root)

[build-system]
requires = ["setuptools==65.7.0", "wheel"]
build-backend = "setuptools.build_meta"

This ensures that any tool (including pip install ., python -m build, or Jenkins calling setup.py) uses setuptools==65.7.0 at build time.

> Note: pip install -e . and setup.py install will still bypass pyproject.toml. So, avoid those if possible.




---

Fix Strategy 2: Pin version explicitly before anything else installs

If modifying pyproject.toml is not an option right now, then add a pre-step in your Jenkinsfile/script:

pip install "setuptools==65.7.0" --upgrade

Do this before anything else runs (like pip install -r requirements.txt or other pip3 install).


---

Temporary Emergency Fix

In your current setup, where pip3 install is used in bulk:

Instead of trying to inject version pins into the cmd string,

You can prefix it like this:


pip install "setuptools==65.7.0" --upgrade && pip3 install ...

This way, it ensures the right version is in place before the main install.


---

Would you like help editing your pyproject.toml or Jenkins pipeline script to include this properly?


