
## Introduction to GitHub Actions

GitHub Actions is a powerful tool that enables you to automate software workflows, such as testing and deployment, right in your GitHub repositories. GitHub Actions provides the ability to build Continuous Integration (CI) and Continuous Deployment (CD) pipelines using YAML configuration files.

### Key Concepts:

1. **Workflows**: A workflow is an automated process that you define in your repository to build, test, and deploy your code. Workflows are defined in `.yml` files in the `.github/workflows/` directory.
   
2. **Jobs**: A workflow is composed of one or more jobs. Each job runs a series of steps on a GitHub-provided runner (or your own self-hosted runner).
   
3. **Steps**: Each job contains multiple steps, and a step can run commands, actions, or shell scripts.

4. **Runners**: A runner is the server that runs your jobs. GitHub offers hosted runners on Linux, Windows, and macOS.

5. **Events**: Workflows are triggered by events, such as a `push` or `pull_request`, which start the workflow execution.

6. **Actions**: Actions are reusable commands or sets of commands that are shared across workflows. GitHub Actions provides a marketplace of pre-built actions that you can include in your workflows.

---

## Creating Your First GitHub Actions Workflow

Let’s walk through creating a simple workflow that automatically runs tests on every push to the repository.

### Step 1: Define the Workflow

In your GitHub repository, create a new directory named `.github/workflows/`. Inside this directory, create a file called `ci.yml` with the following content:

```yaml
name: CI Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - name: Install Dependencies
      run: npm install
    - name: Run Tests
      run: npm test
```

### Explanation:

- **Workflow Name (`name`)**: The name of the workflow, which will appear in GitHub Actions.
- **Triggers (`on`)**: The `push` and `pull_request` events trigger this workflow.
- **Job (`jobs`)**: A job named `build` runs on the latest Ubuntu server (`runs-on: ubuntu-latest`).
- **Steps**:
   1. Check out the code (`actions/checkout@v2`).
   2. Set up Node.js using version 14 (`actions/setup-node@v2`).
   3. Install dependencies using `npm install`.
   4. Run the tests using `npm test`.

### Step 2: Commit and Push

After adding this workflow file to your repository, commit and push your changes. GitHub Actions will automatically start running your workflow when you push or open a pull request.

### Step 3: Monitor Workflow Execution

You can monitor your workflow runs in the "Actions" tab of your repository. Each job and step will display its status, and you can view detailed logs for each step.

---

## Hands-On Activity: Creating a Custom Action

### Step 1: Create a Basic Workflow

Create a file called `.github/workflows/main.yml` in your repository with the following content:

```yaml
name: Custom Action Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Custom Action
      run: echo "Hello, World!"
```

### Step 2: Define a Custom Action

In the root of your repository, create a new directory called `my-action` and add the following files:

- **action.yml**:
   ```yaml
   name: "My Custom Action"
   description: "An action to greet someone"
   inputs:
     name:
       description: "The name of the person to greet"
       required: true
       default: "World"

   runs:
     using: "node12"
     main: "index.js"
   ```

- **index.js**:
   ```js
   console.log(`Hello ${process.env.INPUT_NAME}`);
   ```

### Step 3: Test the Custom Action

Modify the workflow file to use your custom action:

```yaml
name: Custom Action Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Custom Action
      uses: ./my-action
      with:
        name: "Developer"
```

Now, every time you push changes to your repository, your custom action will run and display a personalized greeting.

---

## Test Questions

1. **What is a GitHub Action?**
   - Answer: A GitHub Action is a reusable command used in workflows to automate tasks in your GitHub repository.

2. **What file format is used to define GitHub workflows?**
   - Answer: YAML (.yml or .yaml) is used to define GitHub workflows.

3. **What is the purpose of the `runs-on` key in a job?**
   - Answer: The `runs-on` key specifies the runner or environment (such as `ubuntu-latest`) where the job will run.

4. **How do you trigger a workflow on a `push` event?**
   - Answer: You define `on: push` in the workflow file to trigger it on a push event.

5. **What command is used to set up Node.js in a workflow?**
   - Answer: You use `actions/setup-node@v2` to set up Node.js in a workflow.

---

This Level 1 training provides a foundational understanding of GitHub Actions and hands-on experience in creating workflows and custom actions. In the next level, we will dive deeper into reusable workflows and more advanced GitHub Actions concepts.
