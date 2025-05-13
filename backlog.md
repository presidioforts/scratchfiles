Currently, the CI product’s application‑component onboarding process enforces developers to manually configure 20+ CI property keys in the workflow YAML for each component. This manual YAML editing is error‑prone—leading to typos, misconfigurations, broken builds, and a spike in support tickets—and it slows down onboarding from minutes to hours or days.

We need to enhance the IDP UI so that it:

Auto‑discovers all available CI workflow property keys by buildpack (npm, Gradle, Maven, plain Python, etc.) along with their last‑saved values.

Presents them in a guided, form‑driven interface where developers can view or update values without touching YAML.

Persists those values centrally and, at CI execution time, injects them into the workflow context map automatically.

Mandates that any change to a property value goes through the UI—eliminating hand‑edited YAML as the single point of truth.

This will remove manual configuration pain, prevent build failures, slash support tickets, and restore onboarding to a sub‑15‑minute experience.
