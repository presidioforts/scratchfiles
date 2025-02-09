## Training Data Generation for Sentence Transformer: A DevOps Support Use Case

This document outlines the process for generating high-quality training data for a Sentence Transformer model, specifically tailored for a DevOps support use case. The goal is to create a model capable of effectively performing:

- **Semantic Search**: Finding relevant resolutions for given problems.  
- **Clustering**: Grouping similar problems together.

---

### 1. Data Source

Our primary data source will be raw support ticket information, which typically includes:

- A description of the problem.  
- The resolution provided.  
- (Optional) Additional context about the issue or environment.

---
### 2. Data Transformation Using LLM

We will use a Large Language Model (LLM) to transform the raw support ticket data into a structured JSON format suitable for Sentence Transformer training. The LLM acts as a DevOps support assistant by:

1. Cleaning the data.  
2. Structuring the data.  
3. Enriching the data with any missing but relevant details.

---

### 3. Prompt Engineering
```
You are a DevOps support assistant. Your task is to process raw support ticket data and convert it into a clean, professional, and well-structured format for training a sentence transformer for semantic search and clustering. Follow these steps:

1. Correct Grammar and Spelling: Fix any grammatical errors and spelling mistakes in the text.
2. Improve Clarity and Conciseness: Rewrite sentences to make them clear, concise, and easy to understand. Avoid jargon unless absolutely necessary, and explain it if used. Ensure the language is professional.
3. Add Steps (If Applicable): If the resolution involves multiple steps, break it down into a numbered list. If the resolution is a single action, you don't need a list.
4. Structure the Output: Format the result as a JSON object with "problem", "resolution", "negative_examples" (an array of strings), and "context" (a string, optional) keys. The values should be strings. Use newline characters (`\n`) for line breaks within the resolution text if you have multiple steps. Ensure the JSON is valid.

5. Data Diversity: Where possible, provide multiple variations of the problem and resolution, using different wording and sentence structures. This will improve the diversity of the training data. Aim for at least two variations if feasible.

6. Domain Specificity: While avoiding general jargon, use domain-specific terminology relevant to DevOps and software development when describing problems and resolutions.

Here is an example:

Raw Input:
- Problem: "jenkins EPL build failing when i trigger release build"
- Resolution: "create devops ticket with build build with required log for engineer to troubleshoot. use the JIRA link to report the problem"
- Context: "User is EPL, window worker."

Structured Output:
json
{
  "problem": "jenkins EPL build failing when i trigger release build.",
  "resolution": "create devops ticket with build build with required log for engineer to troubleshoot. use the JIRA link to report the problem.",
  "negative_examples": [
    "The build is running slowly.",
    "The user cannot trigger build."
  ],
  "context": "User is EPL, window worker."
}

Now, process the following raw ticket data:

- Problem: "npm error package angular-2002.05069 version not found"
- Resolution: "check the artifacfory or npm central if the version is and update the available version in package.json. Retrigger the build"
- Context: "User Training" (Optional - if no context, leave blank or put "N/A")
```
```
{
  "problem": "npm error: package angular-2002.05069 version not found.",
  "resolution": "Check the Artifactory or npm Central to verify if the specified version exists. If it does, update the available version in the `package.json` file. Retrigger the build.\n\nAlternatively:\n\nVerify if the package `angular-2002.05069` exists in the Artifactory or npm registry.  If the version is present, ensure the `package.json` file reflects the correct version. After correcting the version, retry the build.",
  "negative_examples": [
    "The build is failing due to a network issue.",
    "The user does not have permissions to access the repository.",
    "The Artifactory server is down."
  ],
  "context": "User Training"
}

```


