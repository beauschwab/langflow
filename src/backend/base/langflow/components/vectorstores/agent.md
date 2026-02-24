# components/vectorstores/ — Vector Store Components

## Purpose
Vector store components for storing and retrieving embeddings in RAG pipelines. Each component integrates with a specific vector database.

## Key Files

| File | Description |
|------|-------------|
| `astradb.py` | DataStax AstraDB vector store. |
| `astradb_graph.py` | AstraDB Graph vector store. |
| `chroma.py` | Chroma vector store. |
| `faiss.py` | FAISS local vector store. |
| `pinecone.py` | Pinecone vector store. |
| `qdrant.py` | Qdrant vector store. |
| `pgvector.py` | PostgreSQL pgvector store. |
| `milvus.py` | Milvus vector store. |
| `mongodb_atlas.py` | MongoDB Atlas vector store. |
| `redis.py` | Redis vector store. |
| `elasticsearch.py` | Elasticsearch vector store. |
| `opensearch.py` | OpenSearch vector store. |
| `supabase.py` | Supabase vector store. |
| `clickhouse.py` | ClickHouse vector store. |
| `couchbase.py` | Couchbase vector store. |
| `cassandra.py` | Apache Cassandra vector store. |
| `cassandra_graph.py` | Cassandra Graph vector store. |
| `hcd.py` | HCD vector store. |
| `graph_rag.py` | Graph RAG vector store. |

## For LLM Coding Agents

- All vector store components extend the base class from `base/vectorstores/model.py`.
- They must implement search and ingest interfaces.
