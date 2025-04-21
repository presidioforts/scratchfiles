
RCA – what’s breaking the build (bullet version)

Node 22 + npm 10.9.2 → npm fetches many “.tgz” package files in parallel

Blue Coat proxy forwards each file to its ICAP virus‑scanner

ICAP times out / refuses scan → returns ICAP_NOT_SCANNED

Proxy converts that into HTTP 520 → npm install fails

Node and npm themselves are fine; block happens entirely inside the proxy path



---

Resolution needed from Network / Security (bullet version)

Bypass the ICAP scan for package files:

Rule: domain = registry.npmjs.org AND URL ends with .tgz → skip ICAP / allow

Alternative: skip ICAP for any traffic coming from Artifactory’s IP/hostname


Keep proxy logging on; only the virus‑scan step is skipped or its timeout raised

CI runners still point to the internal Artifactory repo; no direct Internet access is required once the above rule is active



