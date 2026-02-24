# components/embeddings/ — Embedding Model Components

## Purpose
Text embedding model components for converting text to vector representations, used in RAG pipelines with vector stores.

## Key Files

| File | Description |
|------|-------------|
| `openai.py` | OpenAI embeddings (text-embedding-3-small/large, ada-002). |
| `azure_openai.py` | Azure OpenAI embeddings. |
| `ollama.py` | Ollama local embeddings. |
| `huggingface_inference_api.py` | HuggingFace Inference API embeddings. |
| `amazon_bedrock.py` | AWS Bedrock embeddings. |
| `mistral.py` | Mistral AI embeddings. |
| `vertexai.py` | Google Vertex AI embeddings. |
| `cloudflare.py` | Cloudflare Workers AI embeddings. |
| `aiml.py` | AI/ML embeddings. |
| `astra_vectorize.py` | DataStax Astra vectorize embeddings. |
| `lmstudioembeddings.py` | LM Studio local embeddings. |
| `similarity.py` | Embedding similarity calculation component. |
| `text_embedder.py` | Generic text embedder wrapper. |
