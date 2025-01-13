If you already have your Hugging Face token (HF_TOKEN) handy and just want to verify that it works (e.g., after generating it in JFrog and retrieving it with a password), you can run a quick **test** command against a Hugging Face endpoint that requires authentication. One simple endpoint is `https://huggingface.co/api/whoami`, which will return information about the authenticated user if the token is valid.

Below is a small **bash** snippet you can use to test that your token works:

```bash
#!/bin/bash
##############################################################################
# Test Script: verify-hf-token.sh
# Purpose: Simple check to ensure HF_TOKEN is valid by calling the Hugging Face
#          "whoami" API endpoint.
##############################################################################

# Make sure HF_TOKEN is set (either exported in your shell or passed in)
# e.g.,  export HF_TOKEN="your-hf-token"
# or     HF_TOKEN="your-hf-token" ./verify-hf-token.sh

if [ -z "$HF_TOKEN" ]; then
  echo "ERROR: HF_TOKEN is not set. Please export or provide it."
  exit 1
fi

echo "Testing your Hugging Face token with whoami endpoint..."

# Call Hugging Face "whoami" endpoint
response=$(curl -s -H "Authorization: Bearer $HF_TOKEN" https://huggingface.co/api/whoami)

if [[ "$response" == *"error"* ]]; then
  echo "ERROR: The token might be invalid, or you do not have access."
  echo "Response: $response"
  exit 1
else
  echo "Success! Token is valid."
  echo "Response from whoami:"
  echo "$response"
  exit 0
fi
```

### How to Run This Test

1. **Set your token** in an environment variable:
   ```bash
   export HF_TOKEN="<your-token>"
   ```
2. **Make the script executable**:
   ```bash
   chmod +x verify-hf-token.sh
   ```
3. **Run the script**:
   ```bash
   ./verify-hf-token.sh
   ```

- If the token is valid, you should see a JSON response with your user info.  
- If the token is invalid or missing, you’ll likely get an error.

---

## Quick One-Liner

If you don’t want to use a script file, you can simply do:

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" https://huggingface.co/api/whoami
```

- **Valid token**: Returns a JSON object with something like `"user":{"name":"<your_username>"...}`.  
- **Invalid token**: Returns an error message like `{"error":"Invalid or expired token"}`.

---

### Next Steps

- If you get a **valid** response, you’re good to go—you can then use the same token (`Authorization: Bearer $HF_TOKEN`) in your `curl` commands to download private models or push/pull from HF.
- If you get an **error**, double-check that your token is correct and has not expired. You might need to re-generate it or ensure it has the proper scopes in your [Hugging Face settings](https://huggingface.co/settings/tokens).
