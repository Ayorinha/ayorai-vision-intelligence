# Local-first RAG

The MVP uses a deterministic lexical retriever backed by SQLite so the repository runs without external model APIs or cloud data transfer.

The retrieval interface is provider-neutral. A production deployment can add local embeddings and a vector index behind the same Retriever.search() contract.

The demo knowledge base is synthetic. No proprietary IEPTB material belongs in this public repository.
