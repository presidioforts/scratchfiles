graph TD
    A["Input JSON<br/>(Raw Markdown)"] --> B["Step 1a: Deterministic Cleaning<br/>step1_markdown_cleaner.py"]
    B --> C["Step 1b: Validation<br/>step1_validator.py"]
    C --> D{Records need<br/>LLM processing?}
    D -->|Yes| E["Step 1c: LLM Processing<br/>step2_llm_processor.py"]
    D -->|No| F["✅ Complete!<br/>Perfect Markdown"]
    E --> F
    
    B --> G["Cleaned JSON<br/>(Step 1 Output)"]
    C --> H["Validation Report<br/>(needs_llm flags)"]
    E --> I["Final JSON<br/>(Perfect Markdown)"]
    E --> J["LLM Report<br/>(Processing stats)"]
    
    K["OpenAI API Key<br/>(Required for LLM)"] -.-> E
    
    style A fill:#e1f5fe
    style F fill:#c8e6c9
    style E fill:#fff3e0
    style D fill:#f3e5f5
