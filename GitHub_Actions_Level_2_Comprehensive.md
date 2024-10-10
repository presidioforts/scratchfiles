
## Introduction to Reusable Workflows

In large projects, the need for modular and reusable workflows becomes evident as you scale CI/CD pipelines across repositories. GitHub Actions offers several powerful features, such as reusable workflows and composite actions, to help you achieve that level of efficiency and maintainability.

### Why Reusability Matters:
1. **Consistency**: Enforces consistent CI/CD practices across all repositories.
2. **Efficiency**: Saves time by avoiding repetitive configurations.
3. **Modularity**: Makes workflows more maintainable by separating them into reusable components.

---

## 1. Reusable Workflows in GitHub Actions

Reusable workflows allow you to define a workflow in one repository and reuse it in other repositories. This is particularly helpful when managing multiple repositories that share similar CI/CD tasks.

### Step 1: Define a Reusable Workflow

Create a reusable workflow by adding a file called `reusable-workflow.yml` in the `.github/workflows/` directory:

```yaml
# .github/workflows/reusable-workflow.yml
name: Reusable CI Workflow

on:
  workflow_call:
    inputs:
      env:
        required: true
        type: string

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Check out code
      uses: actions/checkout@v2
    - name: Set up ${{ inputs.env }}
      run: echo "Setting up environment: ${{ inputs.env }}"
    - name: Run tests
      run: npm test
```

### Explanation:
- **workflow_call**: This special event is used to define a workflow that can be called by other workflows.
- **Inputs**: You can define inputs such as `env` to allow flexibility when the workflow is called.

### Step 2: Call the Reusable Workflow

Now that you have defined a reusable workflow, you can invoke it from another repository by using the `uses` keyword:

```yaml
# .github/workflows/main.yml
name: Call Reusable Workflow

on: [push]

jobs:
  call-reusable:
    uses: org/repo/.github/workflows/reusable-workflow.yml@main
    with:
      env: "production"
```

### Explanation:
- **uses**: This specifies the reusable workflow from another repository (e.g., `org/repo`). The reusable workflow is invoked with the input `env` set to "production."

---

## 2. Composite Actions

Composite actions group multiple steps into a reusable action that can be invoked in multiple workflows. This is useful when you want to reuse a set of steps but do not need the complexity of a full reusable workflow.

### Step 1: Create a Composite Action

Define a composite action in a directory named `my-composite-action`:

**action.yml**:
```yaml
name: "Composite Action"
description: "A composite action to set up and run tests"
inputs:
  node-version:
    required: true
    type: string

runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v2
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm install
    - run: npm test
```

### Explanation:
- **Composite Actions**: Composite actions allow you to group multiple steps together. This one sets up Node.js, installs dependencies, and runs tests.

### Step 2: Use the Composite Action

Once you have created the composite action, you can use it in your workflow like this:

```yaml
name: Use Composite Action

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: ./my-composite-action
      with:
        node-version: "14"
```

---

## Best Practices for Reusability

1. **Modularize Workflows**: Break workflows down into smaller components that can be reused across different repositories.
   
2. **Parameterization**: Use inputs to make workflows and actions flexible for different use cases and environments.

3. **DRY Principle**: Avoid repeating yourself by sharing common logic in reusable workflows or composite actions.

---

## Test Questions for Level 2

1. **What event type is used to invoke reusable workflows in GitHub Actions?**
   - Answer: `workflow_call`

2. **What are composite actions used for in GitHub Actions?**
   - Answer: To group multiple steps into a single reusable action.

3. **How do you pass inputs to reusable workflows?**
   - Answer: Define `inputs` in the reusable workflow and pass them when calling the workflow.

---

This Level 2 training provides more advanced concepts around reusability and modular workflows, allowing you to manage larger projects with less duplication and more efficiency.
