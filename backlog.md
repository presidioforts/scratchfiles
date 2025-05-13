Currently, the CI product’s application‑component onboarding requires developers to hand‑edit 20+ workflow property keys in YAML for each component. This manual approach is error‑prone—causing typos, misconfigurations, and broken builds, driving a surge in support tickets—and stretches onboarding from minutes to days.

We need to enhance the **IDP / ELMA UI** to:

* **Auto‑discover** all CI workflow property keys by buildpack (npm, Gradle, Maven, plain Python, etc.) and their last‑saved values
* **Present** them in a guided, form‑driven interface so developers never touch YAML
* **Persist** those values centrally and, at CI execution time, inject them into the workflow context map
* **Enforce** UI‑only edits—eliminating hand‑edited YAML as a source of truth

This will eliminate manual configuration errors, slash support tickets, and restore onboarding to under one hour.

