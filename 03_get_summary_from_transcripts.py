from summary_deepseek_openai import summarize_transcripts

# models = ["qwen2"]
# models = ["gpt-4o-mini"]
# models = ["llama-3.1-70b-versatile", "llama-3.1-405b-reasoning"]
# models = ["llama-3.1-8b-instant"]
models = ["deepseek-chat", "deepseek-coder"]

# Increase Context Length of Ollama or use Groq

for model in models:
    summarize_transcripts(model)
