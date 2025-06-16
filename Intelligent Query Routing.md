## System Design: Intelligent Query Routing

### **1. Architecture Overview**
```
User Query → Router (Llama-3.2-1B) → Decision Engine → Response Synthesis → Single Response
```

### **2. Router Decision Types**
• **HANDLE_DIRECTLY** - Simple queries router can answer
• **SEARCH_NEEDED_INTERNAL_ONLY** - Enterprise docs required
• **SEARCH_NEEDED_BOTH** - Internal + Claude Sonnet needed

### **3. Router Prompt Design**
```
You are a DevOps query router. Analyze the user query and decide how to handle it.

Respond with ONLY one of these options:
- HANDLE_DIRECTLY|[your direct answer]
- SEARCH_NEEDED_INTERNAL_ONLY|[processed query for internal search]  
- SEARCH_NEEDED_BOTH|[processed query for both internal + external]

Decision criteria:
- HANDLE_DIRECTLY: Basic questions, definitions, simple troubleshooting
- INTERNAL_ONLY: CICD, deployments, runbooks, enterprise-specific issues
- BOTH: Complex troubleshooting, multi-system issues, unknown root causes

User Query: {user_input}
```

### **4. Technical Implementation**
• **Single endpoint:** `/v1/chat/completions`
• **Parse router response** by splitting on `|`
• **Execute decision** and synthesize final response

**Does this router prompt structure look right for your use case?**
