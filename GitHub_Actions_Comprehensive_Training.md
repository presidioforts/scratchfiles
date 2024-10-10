
## Introduction to Advanced GitHub Actions Workflows

In this training, we will explore advanced GitHub Actions concepts, building on your knowledge of CI/CD pipelines from Jenkins. These topics will include reusable workflows, matrix builds, caching, secrets management, and more.

### Key Concepts:
1. **Matrix Builds**
2. **Concurrency and Caching**
3. **Job Dependencies**
4. **Environment Protection Rules**
5. **Secrets and Security**
6. **Self-Hosted Runners**
7. **Artifact Management**
8. **Scheduled Workflows (CRON Jobs)**
9. **Custom Docker Container Actions**
10. **Annotations and Logs**
11. **Parallelism**

---

## 1. Matrix Builds

Matrix builds enable running a job across multiple configurations, such as different language versions or operating systems, without duplicating job definitions.

### Example:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [12, 14, 16]
        os: [ubuntu-latest, windows-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: ${{ matrix.node }}
      - run: npm install
      - run: npm test
```
With this, the workflow will run tests for each combination of Node.js versions and operating systems.

---

## 2. Concurrency and Caching

### Concurrency:
Concurrency prevents race conditions by ensuring only a single instance of a workflow runs at a time.
```yaml
concurrency: ci-${{ github.ref }}
```

### Caching:
Use caching to store dependencies between runs, speeding up workflows.
```yaml
- name: Cache Node.js modules
  uses: actions/cache@v2
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

---

## 3. Job Dependencies

Use job dependencies to control the order in which jobs are executed, specifying that a job should wait for another to finish.

### Example:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building"
  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - run: echo "Testing"
```
Here, the `test` job will only run after the `build` job is completed.

---

## 4. Environment Protection Rules

Environment protection allows you to control deployment environments, requiring manual approval before deploying.

### Example:
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://your-production-app.com
    steps:
      - run: echo "Deploying to production"
```
This adds manual approvals for production deployments.

---

## 5. Secrets and Security

Use GitHub Secrets to securely manage sensitive data like API keys or tokens in your workflows.

### Example:
```yaml
steps:
  - name: Deploy
    run: echo "Deploying"
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

---

## 6. Self-Hosted Runners

If you need custom environments or more control over the runners, you can set up self-hosted runners to execute workflows.

### Benefits:
- Full control over runner environments.
- Can run on your infrastructure, reducing costs or using specialized software setups.

---

## 7. Artifact Management

Artifacts allow you to pass data between jobs or share results after workflows are complete.

### Example:
```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v2
  with:
    name: my-artifact
    path: ./path/to/file
```

---

## 8. Scheduled Workflows (CRON Jobs)

Schedule workflows to run at specific times using cron syntax. Useful for tasks like nightly builds or backups.

### Example:
```yaml
on:
  schedule:
    - cron: '0 0 * * *'
```

---

## 9. Custom Docker Container Actions

Create custom Docker container actions to define your environment precisely for running actions.

### Example:
```Dockerfile
FROM node:12
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

---

## 10. Annotations and Logs

GitHub Actions can annotate pull requests, making it easier to review and debug workflows directly from GitHub.

### Example:
```yaml
- name: Annotate Test Results
  run: echo "::warning file=test.txt,line=10::Something went wrong!"
```

---

## 11. Parallelism

You can run multiple jobs or steps in parallel to improve workflow efficiency.

### Example:
```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running Job 1"
  job2:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running Job 2"
```

Both `job1` and `job2` will run in parallel, speeding up the workflow.

---

## Test Questions

1. **What is the purpose of matrix builds in GitHub Actions?**
   - Answer: To run a job across multiple configurations like different versions or environments without duplicating job definitions.

2. **How does caching improve workflow performance in GitHub Actions?**
   - Answer: Caching stores dependencies or artifacts between workflow runs, reducing setup time in subsequent runs.

3. **What does the `needs` keyword do in GitHub Actions?**
   - Answer: It defines job dependencies, ensuring that a job runs only after its required jobs are completed.

4. **What are GitHub Actions environments used for?**
   - Answer: Environments protect deployments by requiring approval or restricting access based on the environment (e.g., staging or production).

5. **How do you store secrets securely in GitHub Actions?**
   - Answer: Secrets can be stored securely using GitHub Secrets, which can be referenced in workflows using `${{ secrets.SECRET_NAME }}`.

---

This concludes the advanced GitHub Actions training. We have covered a wide range of topics that will help you model, optimize, and secure your CI/CD pipelines using GitHub Actions.
