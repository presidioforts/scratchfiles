
End-to-End Guide: Kaniko-Based CI/CD Pipeline with Init Container (Curl) in Kubernetes

A comprehensive guide on using Kaniko in Kubernetes with GitHub Actions, a self-hosted runner, and an Init Container for artifact preparation.


---

Table of Contents

1. Introduction


2. Understanding the Role of Init Container and Kaniko


3. Execution Flow: How It Works


4. GitHub Actions Workflow for Kaniko


5. Kaniko Job YAML with Init Container (Curl)


6. Deploying and Monitoring Kaniko Job


7. Updating Kubernetes Deployment with Built Image


8. Architecture Diagram


9. Best Practices


10. Conclusion




---

1. Introduction

Kaniko is a secure, daemonless image builder for Kubernetes, allowing container builds without requiring privileged access or a running Docker Daemon.

This guide covers: ✅ Using an Init Container (curl) to download artifacts before Kaniko starts.
✅ Setting up a Kubernetes Job to execute Kaniko builds.
✅ Integrating GitHub Actions with a self-hosted runner for automation.
✅ Deploying the built image in Kubernetes.


---

2. Understanding the Role of Init Container and Kaniko


---

3. Execution Flow: How It Works

1️⃣ GitHub Actions triggers a workflow on a self-hosted runner.
2️⃣ Self-hosted runner dynamically generates kaniko.yml and applies it to Kubernetes.
3️⃣ A Kubernetes Pod starts, containing two containers:

Init Container (curl) – Downloads artifacts and prepares the build environment.

Kaniko Container – Waits until Init completes, then builds and pushes the image.
4️⃣ Kaniko pushes the built image to the container registry (ECR, GCR, Artifactory).
5️⃣ GitHub Actions updates the Kubernetes Deployment to use the new image.
6️⃣ Pod terminates after Kaniko completes execution.



---

4. GitHub Actions Workflow for Kaniko

This GitHub Actions YAML runs on a self-hosted runner, generates kaniko.yml, and applies it to Kubernetes.

name: Build and Deploy with Kaniko

on:
  push:
    branches:
      - main

jobs:
  build-image:
    runs-on: self-hosted
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Generate Kaniko Job YAML
        run: |
          cat <<EOF > kaniko.yml
          apiVersion: batch/v1
          kind: Job
          metadata:
            name: kaniko-build
          spec:
            template:
              spec:
                initContainers:
                  - name: curl-container
                    image: curlimages/curl:latest
                    command: ["/bin/sh", "-c"]
                    args:
                      - "curl -k -o /workspace/app.jar https://artifactory.example.com/myapp.jar"
                    volumeMounts:
                      - name: workspace
                        mountPath: /workspace

                containers:
                  - name: kaniko
                    image: gcr.io/kaniko-project/executor:latest
                    args:
                      - --dockerfile=/workspace/Dockerfile
                      - --context=dir://workspace/
                      - --destination=your-registry/your-image:\${{ github.sha }}
                      - --verbosity=debug
                    volumeMounts:
                      - name: workspace
                        mountPath: /workspace

                volumes:
                  - name: workspace
                    emptyDir: {}

                restartPolicy: Never
          EOF

      - name: Apply Kaniko Job in Kubernetes
        run: |
          kubectl apply -f kaniko.yml
          kubectl get jobs

      - name: Wait for Kaniko Job Completion
        run: |
          kubectl wait --for=condition=complete job/kaniko-build --timeout=300s

      - name: Deploy Built Image to Kubernetes
        run: |
          kubectl set image deployment/my-app my-app=your-registry/your-image:\${{ github.sha }}
          kubectl rollout status deployment/my-app


---

5. Kaniko Job YAML with Init Container (curl)

This YAML file dynamically downloads the artifact and builds the image inside Kubernetes.

✔ Init Container (curl) downloads the required artifact (app.jar).
✔ Kaniko builds the image after the Init Container completes.
✔ Uses emptyDir volume for sharing files between Init and Kaniko containers.


---

6. Deploying and Monitoring Kaniko Job

Apply the Job in Kubernetes

kubectl apply -f kaniko.yml
kubectl get jobs

Check Job Logs

kubectl logs -f job/kaniko-build

Verify Image in Registry

docker pull your-registry/your-image:<COMMIT_SHA>


---

7. Updating Kubernetes Deployment with Built Image

Manually Update Deployment

kubectl set image deployment/my-app my-app=your-registry/your-image:<COMMIT_SHA>
kubectl rollout status deployment/my-app

Automate Deployment via GitHub Actions

- name: Deploy Built Image to Kubernetes
  run: |
    kubectl set image deployment/my-app my-app=your-registry/your-image:\${{ github.sha }}
    kubectl rollout status deployment/my-app


---

8. Architecture Diagram

I'll now generate a detailed architecture diagram showing the Init Container, Kaniko Container, and Kubernetes Job interaction.


