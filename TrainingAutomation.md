## Training Data Generation for Sentence Transformer: A DevOps Support Use Case

This document outlines the process for generating high-quality training data for a sentence transformer model, specifically tailored for a DevOps support use case.  The goal is to create a model capable of effectively performing semantic search (finding relevant resolutions for given problems) and clustering (grouping similar problems together).

**1. Data Source:**

Our primary data source will be raw support ticket information, which typically includes a description of the problem, the resolution provided, and sometimes additional context.

**2. Data Transformation using LLM:**

We will use a Large Language Model (LLM) to transform the raw support ticket data into a structured JSON format suitable for sentence transformer training. The LLM acts as a DevOps support assistant, cleaning, structuring, and enriching the data.

**3. Prompt Engineering:**

A carefully crafted prompt is crucial for guiding the LLM to produce the desired output.  The following prompt will be used:

```
You are a DevOps support assistant. Your task is to process raw support ticket data and convert it into a clean, professional, and well-structured format for training a sentence transformer for semantic search and clustering.  Follow these steps:

1. **Correct Grammar and Spelling**: Fix any grammatical errors and spelling mistakes in the text.
2. **Improve Clarity and Conciseness**: Rewrite sentences to make them clear, concise, and easy to understand. Avoid jargon unless absolutely necessary, and explain it if used. Ensure the language is professional.
3. **Add Steps (If Applicable)**: If the resolution involves multiple steps, break it down into a numbered list. If the resolution is a single action, you don't need a list.
4. **Structure the Output**: Format the result as a JSON object with "problem", "resolution", "negative_examples" (an array of strings), and "context" (a string, optional) keys. The values should be strings. Use newline characters (`\n`) for line breaks within the resolution text if you have multiple steps. Ensure the JSON is valid.

5. **Data Diversity:** Where possible, provide multiple variations of the problem and resolution, using different wording and sentence structures. This will improve the diversity of the training data. Aim for at least two variations if feasible.

6. **Domain Specificity:** While avoiding general jargon, use domain-specific terminology relevant to DevOps and software development when describing problems and resolutions.

Here is an example:

Raw Input:
- Problem: "jenkins EPL build failing when i trigger release build"
- Resolution: "create devops ticket with build build with required log for engineer to troubleshoot. use the JIRA link to report the problem"
- Context: "User is EPL, window worker."

Structured Output:
```json
{
  "problem": "jenkins EPL build failing when i trigger release build.",
  "resolution": "create devops ticket with build build with required log for engineer to troubleshoot. use the JIRA link to report the problem.",
  "negative_examples": [
    "The build is running slowly.",
    "The user cannot trigger build."
  ],
    "context": "User is EPL, window worker."
}
```

Now, process the following raw ticket data:

- Problem: "{problem_text}"
- Resolution: "{resolution_text}"
- Context: "{context_text}" (Optional - if no context, leave blank or put "N/A")

```

**4. Sample Input and Output:**

**Raw Input:**

- Problem: "npm error package angular-2002.05069 version not found "
- Resolution: "check the artifacfory or npm central if the version is and update the available version in package.json. Retrigger the build."
- Context: "User Training"

**LLM Generated JSON Output (Example 1):**

```json
{
  "problem": "The npm package 'angular-2002.05069' could not be found.",
  "resolution": "To resolve this issue, follow these steps:\n1. Check your artifact repository or npm central to verify if the specified version of the package exists.\n2. If the version is available, update the 'package.json' file to use the correct version.\n3. Retrigger the build process.",
  "negative_examples": [
    "The Angular application is not compiling.",
    "The user is unable to install other npm packages."
  ],
  "context": "User Training"
}
```

**LLM Generated JSON Output (Example 2 - Variation):**

```json
{
  "problem": "The npm package 'angular-2002.05069' is missing.",
  "resolution": "Resolve this by:\n1. Verifying the package version in your artifact repository or npm central.\n2. Updating the 'package.json' file with the correct, available version.\n3. Rerunning the build.",
  "negative_examples": [
    "The Angular application is not deploying.",
    "There is a problem with the network connection."
  ],
  "context": "User Training"
}
```

**5. Training the Sentence Transformer:**

The generated JSON data will be used to train the sentence transformer model.  The "problem" and "resolution" fields will serve as positive examples, while the "negative_examples" will be used to teach the model to distinguish between related and unrelated issues.  The optional "context" field will provide additional information that the model can leverage.

**6. Benefits:**

* **Improved Semantic Search:** The trained model will be able to find relevant resolutions even if the user's problem description doesn't use the exact same keywords as the stored resolutions.
* **Automated Clustering:** Similar problems can be automatically grouped together, facilitating better organization and analysis of support tickets.
* **Enhanced DevOps Support:**  This will lead to faster resolution times and improved user experience.

**7. Next Steps:**

* Gather and preprocess a large dataset of raw support tickets.
* Refine the LLM prompt as needed based on initial results.
* Train and evaluate the sentence transformer model.
* Integrate the model into the DevOps support workflow.
