# components/models/ — LLM Chat Model Components

## Purpose
Chat model components for connecting to various LLM providers. Each component configures a specific provider's API and returns a LangChain chat model instance.

## Key Files

| File | Description |
|------|-------------|
| `openai_chat_model.py` | OpenAI GPT models (GPT-4, GPT-4o, GPT-3.5). |
| `anthropic.py` | Anthropic Claude models. |
| `ollama.py` | Ollama local models. |
| `azure_openai.py` | Azure-hosted OpenAI models. |
| `amazon_bedrock.py` | AWS Bedrock models. |
| `groq.py` | Groq inference models. |
| `deepseek.py` | DeepSeek models. |
| `mistral.py` | Mistral AI models. |
| `vertexai.py` | Google Vertex AI models. |
| `huggingface.py` | HuggingFace models. |
| `openrouter.py` | OpenRouter multi-provider gateway. |
| `perplexity.py` | Perplexity AI models. |
| `sambanova.py` | SambaNova models. |
| `novita.py` | Novita AI models. |
| `aiml.py` | AI/ML API models. |
| `lmstudiomodel.py` | LM Studio local models. |
| `maritalk.py` | MariTalk models. |
| `baidu_qianfan_chat.py` | Baidu Qianfan models. |
| `language_model.py` | Generic language model wrapper. |

## For LLM Coding Agents

- All model components extend `LCModelComponent` from `base/models/model.py`.
- To add a new provider: create a component file here, add provider constants to `base/models/`, export in `__init__.py`.
