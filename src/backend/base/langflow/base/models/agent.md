# base/models/ — LLM Model Base Class

## Purpose
Defines the `LCModelComponent` base class for all LLM/chat model components. Also contains provider-specific constant definitions for model names, parameters, and configurations.

## Key Files

| File | Description |
|------|-------------|
| `model.py` | `LCModelComponent` base class — standard interface for chat model components with streaming, tool calling, and structured output support. |
| `model_utils.py` | Model utility functions. |
| `model_input_constants.py` | Shared input field constants used across model components. |
| `chat_result.py` | Chat result processing utilities. |
| `openai_constants.py` | OpenAI model name lists and defaults. |
| `anthropic_constants.py` | Anthropic model name lists and defaults. |
| `aws_constants.py` | AWS Bedrock model constants. |
| `google_generative_ai_constants.py` | Google Gemini model constants. |
| `groq_constants.py` | Groq model constants. |
| `ollama_constants.py` | Ollama model constants. |
| `sambanova_constants.py` | SambaNova model constants. |
| `novita_constants.py` | Novita AI model constants. |
| `aiml_constants.py` | AI/ML model constants. |

## For LLM Coding Agents

- When adding a new LLM provider, create a constants file here and a component in `components/models/`.
- `LCModelComponent` handles streaming, tool calling, and message formatting automatically.
