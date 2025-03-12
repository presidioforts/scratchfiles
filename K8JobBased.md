---

# Image Scanning Infrastructure: Using Crane and Twist CLI for Security Analysis

## 1. Introduction
Container security plays a vital role in modern DevOps pipelines. This document details how to:

- Pull container images **daemonlessly** using **Crane**.  
- Scan those images for **vulnerabilities** using **Twist CLI**.  
- Automate the entire process in a **Kubernetes Job**, ensuring reproducible and auditable scans.

### Overview of the Process
1. **Crane** pulls the image from a registry, consolidating layers into a tarball.  
2. **Twist CLI** scans the tarball for vulnerabilities and compliance issues.  
3. Results can be **uploaded** to an external repository (e.g., Artifactory) for **audit** and **compliance**.

---

## 2. Tools Overview

### 2.1 Crane
- **What Is Crane?**  
  A lightweight, daemonless tool that interacts with container registries (pulling, extracting, manipulating images) without needing Docker.

- **Why Use Crane?**  
  - **Daemonless** operation – No need to run Docker in your CI environment.  
  - **Efficient** handling of OCI layers.  
  - **Lightweight** – Minimal overhead in Kubernetes/CI/CD.

### 2.2 Twist CLI
- **What Is Twist CLI?**  
  The Prisma Cloud command-line interface for scanning images for vulnerabilities, compliance, and misconfigurations.

- **Why Use Twist CLI?**  
  - **Integrated** with Prisma Cloud threat intelligence.  
  - **Automated** scanning in CI/CD (exit with error on high-severity findings).  
  - **Versatile** – Scans tarballs, local images, or remote registries.

---

## 3. The Complete Kubernetes Job YAML

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: crane-image-scan-job
  annotations:
    sidecar.istio.io/inject: "false"
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never

      volumes:
        - name: certs
          configMap:
            name: cloud-proxy-cert
        - name: artifactory-registry-cred
          secret:
            secretName: regcred-combined
            items:
              - key: .dockerconfigjson
                path: config.json
        - name: docker-file-storage
          emptyDir: {}
        - name: workspace
          emptyDir: {}

      initContainers:
        - name: crane-init
          image: wfcertifiedvirtual.<registry>/ciwat-crane:debug
          command: ["/bin/sh", "-c"]
          args:
            - |
              # 1) Authenticate with private registry
              /ko-app/crane auth login \
                -u <REGISTRY_USER> -p <REGISTRY_PASS> \
                <registry> --insecure --verbose

              # 2) Pull the target image, saving it to /workspace
              /ko-app/crane pull --insecure --verbose \
                <registry>/<image>:<tag> /workspace/app.tar

              # 3) Verify that the tar file is present
              ls -l /workspace
          volumeMounts:
            - name: artifactory-registry-cred
              mountPath: /crane/docker
            - name: docker-file-storage
              mountPath: /crane/docker-file-storage
            - name: workspace
              mountPath: /workspace

      containers:
        - name: crane-scan
          image: wfcertifiedvirtual.<registry>/gitact-curl:latest
          imagePullPolicy: Always
          command: ["/bin/sh", "-c"]
          args:
            - |
              # 1) Set proxy environment variables if required
              export HTTP_PROXY=http://cloudproxy.mycompany.net:80
              export HTTPS_PROXY=http://cloudproxy.mycompany.net:80
              export NO_PROXY=".mycompany.net"

              # 2) Download Twist CLI
              curl -L -o twistcli https://<prisma-cloud-url>/api/v1/twistcli
              chmod +x twistcli

              # 3) Update custom CA certificates (optional if using internal CA)
              update-ca-certificates

              echo "Starting Prisma Cloud Twist CLI scan..."

              # 4) Run Twist CLI scan on the tarball
              ./twistcli images scan --address <prisma-cloud-url> \
                --user <twist_user> --password <twist_pass> \
                --tarball /workspace/app.tar \
                --output-file /workspace/scan-results.json \
                --details

              exit_code=$?
              if [ "$exit_code" -ne 0 ]; then
                echo "Warning: Twist CLI scan encountered issues (exit code: $exit_code)."
              else
                echo "Twist CLI scan completed successfully."
              fi

              # 5) (Optional) Upload scan results to Artifactory
              curl -X PUT \
                "https://artifactory.mycompany.net/artifactory/maven-local/scan-reports/scan-results.json" \
                -T /workspace/scan-results.json

              # 6) Exit with the Twist CLI status code
              exit $exit_code
          env:
            - name: DOCKER_CONFIG
              value: /crane/docker
          volumeMounts:
            - name: certs
              mountPath: /usr/local/share/ca-certificates/<custom-ca>.cer
              subPath: <custom-ca>.cer
            - name: artifactory-registry-cred
              mountPath: /crane/docker
            - name: docker-file-storage
              mountPath: /crane/docker-file-storage
            - name: workspace
              mountPath: /workspace
```

---

## 4. Step-by-Step Breakdown of the YAML

Here is a **detailed explanation** of each section in the manifest, clarifying **how** it works and **why** each step is necessary.

### 4.1 Job Metadata and Spec

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: crane-image-scan-job
  annotations:
    sidecar.istio.io/inject: "false"
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never
```

- **apiVersion, kind**: Identifies this resource as a Kubernetes `Job`.  
- **metadata.name**: The name (e.g., `crane-image-scan-job`) for referencing the Job.  
- **annotations.sidecar.istio.io/inject: "false"**: Prevents Istio from injecting a sidecar proxy if Istio is in the cluster.  
- **spec.backoffLimit: 0**: Specifies **no retries** on failure. A single failure results in the Job ending in error.  
- **restartPolicy: Never**: Ensures pods are not restarted on completion or failure, appropriate for one-off tasks.

### 4.2 Volumes Definition

```yaml
volumes:
  - name: certs
    configMap:
      name: cloud-proxy-cert
  - name: artifactory-registry-cred
    secret:
      secretName: regcred-combined
      items:
        - key: .dockerconfigjson
          path: config.json
  - name: docker-file-storage
    emptyDir: {}
  - name: workspace
    emptyDir: {}
```

- **certs (ConfigMap)**: Holds custom CA certificates if needed (internal self-signed or corporate CA).  
- **artifactory-registry-cred (Secret)**: Contains `.dockerconfigjson` credentials for pulling images from private registries.  
- **docker-file-storage (EmptyDir)**: Temporary storage for any Crane Docker-based operations.  
- **workspace (EmptyDir)**: A critical shared space where the init container saves the tarball (`app.tar`) and the main container reads it for scanning.

### 4.3 Init Container (Crane Pull)

```yaml
initContainers:
  - name: crane-init
    image: wfcertifiedvirtual.<registry>/ciwat-crane:debug
    command: ["/bin/sh", "-c"]
    args:
      - |
        # 1) Authenticate with private registry
        /ko-app/crane auth login \
          -u <REGISTRY_USER> -p <REGISTRY_PASS> \
          <registry> --insecure --verbose

        # 2) Pull the target image, saving it to /workspace
        /ko-app/crane pull --insecure --verbose \
          <registry>/<image>:<tag> /workspace/app.tar

        # 3) Verify that the tar file is present
        ls -l /workspace
    volumeMounts:
      - name: artifactory-registry-cred
        mountPath: /crane/docker
      - name: docker-file-storage
        mountPath: /crane/docker-file-storage
      - name: workspace
        mountPath: /workspace
```

1. **Authenticate with the registry**: Uses credentials from the `artifactory-registry-cred` secret (`.dockerconfigjson`).  
2. **Pull the container image** via Crane into `/workspace/app.tar`.  
3. **Verify** the tar file’s presence.  
4. Because it’s an **initContainer**, it **must** finish before the main container starts. A failure here halts the entire Job, preventing scans on an invalid or absent image.

### 4.4 Main Container (Twist CLI Scan)

```yaml
containers:
  - name: crane-scan
    image: wfcertifiedvirtual.<registry>/gitact-curl:latest
    ...
    args:
      - |
        # 1) Set proxy environment variables if needed
        export HTTP_PROXY=http://cloudproxy.mycompany.net:80
        export HTTPS_PROXY=http://cloudproxy.mycompany.net:80
        export NO_PROXY=".mycompany.net"

        # 2) Download Twist CLI
        curl -L -o twistcli https://<prisma-cloud-url>/api/v1/twistcli
        chmod +x twistcli

        # 3) Update custom CA certificates
        update-ca-certificates

        echo "Starting Prisma Cloud Twist CLI scan..."

        # 4) Scan the tarball
        ./twistcli images scan --address <prisma-cloud-url> \
          --user <twist_user> --password <twist_pass> \
          --tarball /workspace/app.tar \
          --output-file /workspace/scan-results.json \
          --details

        exit_code=$?
        if [ "$exit_code" -ne 0 ]; then
          echo "Warning: Twist CLI scan encountered issues (exit code: $exit_code)."
        else
          echo "Twist CLI scan completed successfully."
        fi

        # 5) (Optional) Upload results
        curl -X PUT \
          "https://artifactory.mycompany.net/artifactory/maven-local/scan-reports/scan-results.json" \
          -T /workspace/scan-results.json

        # 6) Exit with Twist CLI status
        exit $exit_code
    ...
```

1. **Set Proxy Variables**: Ensures that if your environment requires HTTP/HTTPS proxy, Crane/Twist CLI can reach external endpoints (like Prisma Cloud).  
2. **Download Twist CLI**: Pulled from your Prisma Cloud console’s URL and made executable.  
3. **Update CA Certificates**: Only necessary if your environment uses custom or internal certificate authorities.  
4. **Scan the Tarball**:  
   - `--tarball /workspace/app.tar` instructs Twist CLI to scan the locally pulled image.  
   - `--output-file /workspace/scan-results.json` captures detailed vulnerability data.  
5. **Capture Exit Code**:  
   - Logs a warning if `exit_code != 0`.  
   - You can fail the Job automatically if critical issues are found (since `exit $exit_code` will propagate that status).  
6. **Optional Upload**:  
   - Uses `curl -X PUT` to push the JSON results to Artifactory or another external repository.

---

## 5. Putting It All Together

When you run:
```bash
kubectl apply -f crane-twistcli-scan-job.yaml
```
Kubernetes creates a **Job** with one Pod that has:
1. **Init Container**  
   - Authenticates and pulls `<registry>/<image>:<tag>` into `/workspace/app.tar`.  
   - Must succeed or the Job fails immediately.
2. **Main Container**  
   - Downloads Twist CLI.  
   - Scans the tarball.  
   - Logs success or failure.  
   - (Optional) Uploads results to Artifactory.

**Result**: A **consistent** and **isolated** scanning workflow. If Twist CLI identifies severe vulnerabilities, you can configure your CI/CD to **stop** further deployment steps.

---

## 6. Best Practices

1. **Use Secrets for All Credentials**  
   - Store Docker credentials (`.dockerconfigjson`) and Twist CLI credentials (user/password) in Kubernetes Secrets.  
   - Never hardcode sensitive data in plaintext.

2. **Fail Fast on Critical Vulnerabilities**  
   - Let the Job exit non-zero to block any further pipeline steps if a scan detects serious issues.

3. **Manage Resources Properly**  
   - Pulling and scanning large images may consume more CPU/memory. Specify proper `requests` and `limits` in your Job.

4. **Centralize Logs & Reports**  
   - Preserve `scan-results.json` in Artifactory, Amazon S3, or another store for compliance and future audits.

5. **Pod Security & CA Certificates**  
   - If behind a corporate proxy, ensure environment variables (`HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`) are correct.  
   - If using internal CAs, mount them from a ConfigMap and run `update-ca-certificates`.

6. **Reproducibility & Scalability**  
   - You can replicate this Job for different images.  
   - For parallel scanning, you might create multiple Jobs or scale out a CronJob to handle scheduled scans.

---

## 7. Conclusion

By combining **Crane** (for daemonless image pulling) and **Twist CLI** (for vulnerability scanning) in a single Kubernetes Job:

- You **eliminate** the need for a Docker daemon in your pipeline.  
- You ensure **early detection** of vulnerabilities, preventing compromised images from moving downstream.  
- You gain **auditable reports**, ensuring compliance and traceability for each scanned image.

This design is both **modular** (init container for pulling, main container for scanning) and **secure** (failure on high-severity issues), making it ideal for production-grade DevOps pipelines.
