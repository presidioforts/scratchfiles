## Image Scanning Infrastructure: Using Crane and Twist CLI for Security Analysis

### Introduction
Ensuring container security is a critical aspect of DevOps pipelines. This document provides a detailed guide on how we utilize Crane and Twist CLI for downloading, packaging, and scanning container images to detect vulnerabilities before deployment.

#### Overview of the Process
1. **Download container images using Crane** – This fetches all image layers and combines them into `app.tar`.  
2. **Download Twist CLI** – This is the CLI client for Prisma Cloud, used for image vulnerability scanning.  
3. **Upload `app.tar` and execute Twist CLI scan** – This analyzes the container image for security risks.

---

## Tool: Crane for Container Image Download

### What is Crane?
Crane is a lightweight tool for interacting with container registries. It allows downloading container images, extracting files, and manipulating OCI-compliant images without a local Docker daemon.

### Why Use Crane?
- ✅ Daemonless operation – No need for a running Docker service.  
- ✅ Efficient image layer handling – Directly downloads image layers.  
- ✅ Lightweight and fast – Optimized for Kubernetes environments.

### Downloading a Container Image Using Crane
```bash
# Authenticate with private registry (if required)
crane auth login my-registry.com --username <user> --password <password>

# Pull the image layers and store in a tar file
crane pull my-registry.com/my-image:latest my-image.tar

# Verify image contents
tar -tvf my-image.tar
```

### Combining Image Layers into `app.tar`
```bash
# Extract image layers (optional step for inspection)
tar -xvf my-image.tar -C extracted_layers/

# Repackage all layers into app.tar
mv my-image.tar app.tar
```

---

## Tool: Twist CLI for Image Scanning

### What is Twist CLI?
Twist CLI is the command-line tool for Prisma Cloud, allowing security scans on container images for known vulnerabilities.

### Why Use Twist CLI?
- ✅ Prisma Cloud integration – Detects vulnerabilities, misconfigurations, and compliance violations.  
- ✅ Automated security scanning – Can be integrated into CI/CD pipelines.  
- ✅ Supports local and remote image scanning.

### Downloading Twist CLI
```bash
# Download Twist CLI (example for Linux)
curl -L -o twistcli https://<prisma-cloud-url>/api/v1/twistcli
chmod +x twistcli
mv twistcli /usr/local/bin/

# Validate Prisma Cloud API connectivity
curl -k https://<prisma-cloud-url>/api/v1/health
```

---

## Image Scanning with Twist CLI

### Uploading and Scanning the Image
```bash
# Upload the app.tar file and scan it
twistcli images scan --address <prisma-cloud-url> --user <username> --password <password> app.tar
```

### Interpreting the Scan Results
- **High-severity vulnerabilities** → Immediate action required.  
- **Medium/low-severity vulnerabilities** → Should be reviewed based on security policies.  
- **Compliance violations** → Recommendations provided for fixing misconfigurations.

**_Suggestion:_** *Consider how you’ll handle large images or scanning timeouts in high-traffic environments. For instance, documenting retry intervals or memory constraints for scanning tools can preempt performance issues in production.*

---

## Summary of the Image Scanning Process

| **Step** | **Tool**   | **Description**                                                                       |
|----------|------------|---------------------------------------------------------------------------------------|
| 1        | Crane      | Downloads the container image layers and saves as `app.tar`.                          |
| 2        | Twist CLI  | Downloads the security scanning tool for Prisma Cloud.                                |
| 3        | Twist CLI  | Uploads `app.tar` and scans it for vulnerabilities.                                   |

---

## Best Practices for Secure Image Handling

- ✅ Use `crane auth login` for private registries.  
- ✅ Verify tarball integrity (`tar -tvf my-image.tar`) before scanning.  
- ✅ Use `--platform=linux/amd64` when pulling multi-arch images.  
- ✅ Enable logging and retries for Twist CLI.  

**_Suggestion:_** *Integrate Twist CLI scanning into your CI/CD pipeline so the build fails automatically if critical vulnerabilities are discovered. This helps ensure only secure images progress to production.*

---

## Conclusion
By integrating Crane for image retrieval and Twist CLI for security scanning, we ensure container images are safe before deployment. This setup prevents security vulnerabilities from entering production environments and enhances compliance with security best practices.

**_Suggestion:_** *Include a brief reference to pipeline exit codes or error-handling strategies (e.g., failing the build on high-severity findings) to tighten the overall process.*
