
import openai
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import uuid

# Setup OpenAI
openai.api_key = "your-openai-key"

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Sample input
user_text = "Hi, my name is John Smith and my phone number is 123-456-7890."

# Step 1: Analyze PII
analysis_results = analyzer.analyze(text=user_text, language="en")

# Step 2: Create placeholder-based anonymization
placeholder_map = {}
anonymized_text = user_text
offset_shift = 0

for idx, result in enumerate(sorted(analysis_results, key=lambda x: x.start)):
    entity_type = result.entity_type
    original_text = user_text[result.start:result.end]
    placeholder = f"<{entity_type}_{idx+1}>"

    # Save mapping
    placeholder_map[placeholder] = original_text

    # Replace in text manually
    start = result.start + offset_shift
    end = result.end + offset_shift
    anonymized_text = anonymized_text[:start] + placeholder + anonymized_text[end:]
    offset_shift += len(placeholder) - len(original_text)

print("\nAnonymized Text:", anonymized_text)
print("PII Map:", placeholder_map)

# Step 3: Call OpenAI API
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": anonymized_text}],
    temperature=0
)
llm_output = response["choices"][0]["message"]["content"]

print("\nLLM Response (Anonymized):", llm_output)

# Step 4: De-anonymize the LLM response
def restore_pii(text, mapping):
    for placeholder, pii_value in mapping.items():
        text = text.replace(placeholder, pii_value)
    return text

final_response = restore_pii(llm_output, placeholder_map)

print("\nFinal Response (With PII):", final_response)
