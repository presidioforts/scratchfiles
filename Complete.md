Kainiko Job YAML Documentation

This document provides a structured breakdown, step-by-step execution flow, and a guide for modifying/customizing the Kainiko job YAML.


---

1. Structured Breakdown of YAML Components

1.1 Metadata and Job Definition

apiVersion: batch/v1
kind: Job
metadata:
  annotations: {}
  name: kaniko-${{ env.UNIQUE_ID }}

apiVersion: batch/v1 – Specifies that this is a Kubernetes batch job.

kind: Job – Defines the resource as a Kubernetes Job.

metadata.name – Unique job name, dynamically set using the UNIQUE_ID environment variable.



---

1.2 Job Specification

spec:
  backoffLimit: 0

backoffLimit: 0 – Ensures the job doesn’t retry on failure.



---

1.3 Pod Template Metadata

template:
    metadata:
      annotations:
        sidecar.istio.io/inject: "false"

Disables Istio sidecar injection if Istio is enabled in the cluster.



---

1.4 Volumes for Configuration and Build Artifacts

spec:
      volumes:
        - name: artifactory-registry-cred
          secret:
            secretName: ${{ fromJson(steps.kf-config.outputs.resultValue).image.arti.secret_name }}
            items:
              - key: .dockerconfigjson
                path: config.json
        - name: docker-file-storage
          emptyDir: {}

artifactory-registry-cred – Stores Docker authentication credentials.

docker-file-storage – Temporary storage for build artifacts.



---

1.5 Container Definition for Kaniko

containers:
        - name: kaniko-${{ env.UNIQUE_ID }}
          image: ${{ fromJson(steps.kf-config.outputs.resultValue).container_registry.clusters.kfcr_certified.url }}/gitact-kaniko:${{ fromJson(steps.kf-config.outputs.resultValue).image.version.kaniko }}
          imagePullPolicy: Always

image – Kaniko container image retrieved dynamically.

imagePullPolicy: Always – Always pulls the latest Kaniko image.



---

1.6 Kaniko Build Arguments

args:
            - --dockerfile=/workspace/Dockerfile
            - --destination=${{ fromJson(steps.kf-config.outputs.resultValue).container_registry.clusters.kfcr_scratch.url }}/IMAGE_NAME
            - --skip-tls-verify
            - --verbosity=debug

--dockerfile – Points to the generated Dockerfile.

--destination – Defines the registry destination for the built image.

--skip-tls-verify – Bypasses TLS verification for private registries.

--verbosity=debug – Enables detailed logging.



---

1.7 Labels for Build Metadata

- --label=company.com/build.url=${{ env.BUILD_URL }}
            - --label=company.com/app.id=${{ env.APP_ID }}
            - --label=company.com/app.version=${{ steps.unique-tag.outputs.APP_VERSION }}
            - --label=company.com/build.artifact.version=${{ env.RELEASE_NUMBER }}
            - --label=company.com/build.number=${{ env.BUILD_NUMBER }}
            - --label=company.com/build.component.name=${{ env.BUILD_COMPONENT_NAME }}

Adds metadata labels to the container for tracking.



---

1.8 Environment Variables

env:
        - name: DOCKER_CONFIG
          value: /kaniko/.docker/

Sets DOCKER_CONFIG for authentication.



---

1.9 Resource Limits

resources:
        requests:
          cpu: 100m
          memory: 1Gi
        limits:
          cpu: 100m
          memory: 4Gi

Defines CPU and memory limits for the container.



---

1.10 Init Container for Artifact Retrieval

initContainers:
        - name: kaniko-init
          image: ${{ fromJson(steps.kf-config.outputs.resultValue).container_registry.clusters.kfcr_certified.url }}/gitact-curl:latest
          imagePullPolicy: Always

Runs before the Kaniko container to download necessary artifacts.



---

1.11 Init Container Execution Script

command:
            - sh
            - -c
            - |
              echo "Request URL to download: ${{ steps.published-artifact-url.outputs.DOWNLOAD_ARTIFACTORY_URL }}"

Prints the artifact download URL.

Executes different logic based on the artifact type (.NET, JAR, WAR).



---

2. Step-by-Step Execution Flow

2.1 Job Execution

1. Kubernetes creates a job using this YAML.


2. The Init Container starts:

Downloads the required artifact from Artifactory.

Determines the artifact type (.NET DLL, JAR, or WAR).

Generates a Dockerfile dynamically.



3. The Kaniko container starts:

Reads the generated Dockerfile.

Builds the container image.

Pushes the image to the registry.



4. Job completes successfully if the image push succeeds.




---

3. Developer Guide for Modifications

3.1 Changing the Destination Registry

Modify:

- --destination=${{ fromJson(steps.kf-config.outputs.resultValue).container_registry.clusters.kfcr_scratch.url }}/IMAGE_NAME

Replace kfcr_scratch.url with another registry.


---

3.2 Adding Support for More Artifact Types

Extend the init container script:

elif [ "${{ steps.artifact-type.outputs.ARTIFACTTYPE }}" == "tar.gz" ]; then
  curl -X GET "${{ steps.published-artifact-url.outputs.DOWNLOAD_ARTIFACTORY_URL }}" -o app.tar.gz
  tar -xzf app.tar.gz -C /workspace

Adds handling for .tar.gz artifacts.



---

3.3 Adjusting Resource Limits

Modify:

resources:
        requests:
          cpu: 200m
          memory: 2Gi
        limits:
          cpu: 500m
          memory: 6Gi

Increases memory allocation for larger builds.



---

3.4 Enabling TLS Verification

Remove:

- --skip-tls-verify

Forces TLS validation for registry authentication.



---

3.5 Adding a Post-Build Notification

Modify the Kaniko container:

args:
            - --post-build-hook="curl -X POST -H 'Content-Type: application/json' -d '{\"status\": \"success\"}' http://notification-service/"

Sends a webhook to notify external services when a build completes.



---

4. Summary

This Kainiko job YAML automates the build and push of Docker images.

Supports .NET, JAR, and WAR artifacts with dynamic Dockerfile generation.

Can be modified to support new artifact types, registries, and build optimizations.



---

Next Steps

Would you like:

1. A sample test scenario to validate this YAML in a Kubernetes cluster?


2. Integration documentation for CI/CD (e.g., GitHub Actions or Jenkins)?



Let me know how you'd like to proceed!

