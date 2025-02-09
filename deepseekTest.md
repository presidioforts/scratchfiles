C:\Users\ollama>ollama list
NAME               ID              SIZE      MODIFIED
deepseek-r1:8b     28f8fd6cdc67    4.9 GB    6 days ago
llama3.2:latest    a80c4f17acd5    2.0 GB    6 days ago

C:\Users\ollama>ollama show deepseek-r1:8b
  Model
    architecture        llama
    parameters          8.0B
    context length      131072
    embedding length    4096
    quantization        Q4_K_M

  Parameters
    stop    "<｜begin▁of▁sentence｜>"
    stop    "<｜end▁of▁sentence｜>"
    stop    "<｜User｜>"
    stop    "<｜Assistant｜>"

  License
    MIT License
    Copyright (c) 2023 DeepSeek


C:\Users\ollama>ollama
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.

C:\Users\ollama>ollama list
NAME               ID              SIZE      MODIFIED
deepseek-r1:8b     28f8fd6cdc67    4.9 GB    6 days ago
llama3.2:latest    a80c4f17acd5    2.0 GB    6 days ago

C:\Users\ollama>ollama run llama3.2:latest
>>> You are a DevOps support assistant. Your task is to process raw support ticket data and convert it into a clean, pro
... fessional, and well-structured format for training a sentence transformer for semantic search and clustering. Follow
...  these steps:
...
... 1. Correct Grammar and Spelling: Fix any grammatical errors and spelling mistakes in the text.
... 2. Improve Clarity and Conciseness: Rewrite sentences to make them clear, concise, and easy to understand. Avoid jar
... gon unless absolutely necessary, and explain it if used. Ensure the language is professional.
... 3. Add Steps (If Applicable): If the resolution involves multiple steps, break it down into a numbered list. If the
... resolution is a single action, you don't need a list.
... 4. Structure the Output: Format the result as a JSON object with "problem", "resolution", "negative_examples" (an ar
... ray of strings), and "context" (a string, optional) keys. The values should be strings. Use newline characters (`\n`
... ) for line breaks within the resolution text if you have multiple steps. Ensure the JSON is valid.
...
... 5. Data Diversity: Where possible, provide multiple variations of the problem and resolution, using different wordin
... g and sentence structures. This will improve the diversity of the training data. Aim for at least two variations if
... feasible.
...
... 6. Domain Specificity: While avoiding general jargon, use domain-specific terminology relevant to DevOps and softwar
... e development when describing problems and resolutions.
...
... Here is an example:
...
... Raw Input:
... - Problem: "jenkins EPL build failing when i trigger release build"
... - Resolution: "create devops ticket with build build with required log for engineer to troubleshoot. use the JIRA li
... nk to report the problem"
... - Context: "User is EPL, window worker."
...
... Structured Output:
... json
... {
...   "problem": "jenkins EPL build failing when i trigger release build.",
...   "resolution": "create devops ticket with build build with required log for engineer to troubleshoot. use the JIRA
... link to report the problem.",
...   "negative_examples": [
...     "The build is running slowly.",
...     "The user cannot trigger build."
...   ],
...   "context": "User is EPL, window worker."
... }
...
... Now, process the following raw ticket data:
...
... - Problem: "{problem_text}"
... - Resolution: "{resolution_text}"
... - Context: "{context_text}" (Optional - if no context, leave blank or put "N/A")
I'd be happy to help you process the raw support ticket data. Here's an example of how I would structure the
output as a JSON object:

Please provide the raw ticket data, including the problem text, resolution text, and context text (if applicable).
I'll then convert it into a clean, professional, and well-structured format for training a sentence transformer
for semantic search and clustering.

>>> Problem: npm error package angular-2002.05069 version not found
... Resolution: check the artifacfory or npm central if the version is and update the available version in package.json.
...  Retrigger the build.
... Context: User Training
Here's the processed data:

```json
{
  "problem": "npm error package angular-2002.05069 version not found.",
  "resolution": "check the artifactory or npm central if the version is available and update the available version in package.json. retrigger
the build.",
  "negative_examples": [
    "The package cannot be installed due to a version mismatch.",
    "There is no valid version of the Angular package."
  ],
  "context": "User Training"
}
```

I made two variations of the problem and resolution to improve data diversity:

```json
{
  "problem": "npm error: unable to find package angular@2002.05069",
  "resolution": "verify the artifactory or npm central repository for the specified Angular version and update the version in package.json
before retriggering the build.",
  "negative_examples": [
    "The Angular package cannot be installed due to a missing version.",
    "No valid version of Angular is available."
  ],
  "context": "User Training"
}
```

Let me know if you'd like me to process more data or make any further adjustments!

>>> Send a message (/? for help)
