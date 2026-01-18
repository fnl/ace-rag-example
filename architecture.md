# Architecture

This document describes the architecture of the RAG (Retrieval-Augmented Generation) service.

## Components

- **Admin Client**: Administrative interface for bulk document operations
- **User Client**: End-user interface for querying documents
- **API Server**: Handles requests and orchestrates the RAG pipeline
- **Vector Store**: Stores and retrieves document embeddings, delegates to Embedding Service
- **Embedding Service**: Converts text to vector embeddings (accessed only via Vector Store)
- **LLM Service**: Generates responses using retrieved context

## Process 1: Bulk Document Upsert

An admin user uploads documents to be indexed in the vector store. The system checks for existing documents and only updates those that have been modified.

```mermaid
sequenceDiagram
    participant Admin as Admin Client
    participant API as API Server
    participant VS as Vector Store
    participant Embed as Embedding Service

    Admin->>API: POST /admin/documents (bulk documents)
    API->>API: Validate request & authenticate admin

    loop For each document
        API->>API: Compute document hash
        API->>VS: Check if document exists (by ID)
        VS-->>API: Return existing document metadata (if any)

        alt Document is new
            API->>API: Chunk document into segments
            API->>VS: Insert chunks
            VS->>Embed: Generate embeddings for chunks
            Embed-->>VS: Return embedding vectors
            VS->>VS: Store chunks with embeddings
            VS-->>API: Confirm insert complete
        else Document exists and hash differs
            API->>VS: Delete existing chunks for document
            VS-->>API: Confirm deletion
            API->>API: Chunk document into segments
            API->>VS: Insert chunks
            VS->>Embed: Generate embeddings for chunks
            Embed-->>VS: Return embedding vectors
            VS->>VS: Store chunks with embeddings
            VS-->>API: Confirm insert complete
        else Document exists and hash matches
            API->>API: Skip (no changes needed)
        end
    end

    API-->>Admin: 200 OK (inserted, updated, skipped counts)
```

## Process 2: User Document Query

A user queries the system to retrieve relevant documents and get a generated response.

```mermaid
sequenceDiagram
    participant User as User Client
    participant API as API Server
    participant VS as Vector Store
    participant Embed as Embedding Service
    participant LLM as LLM Service

    User->>API: POST /query (user question)
    API->>API: Validate request

    API->>VS: Search similar documents (query text, top-k)
    VS->>Embed: Generate embedding for query
    Embed-->>VS: Return query embedding vector
    VS->>VS: Perform similarity search
    VS-->>API: Return matching chunks with scores

    API->>API: Build prompt with retrieved context
    API->>LLM: Generate response (prompt + context)
    LLM-->>API: Return generated answer

    API-->>User: 200 OK (answer, source references)
```

## Process 3: Document Deletion

An admin user deletes documents and their associated chunks from the vector store.

```mermaid
sequenceDiagram
    participant Admin as Admin Client
    participant API as API Server
    participant VS as Vector Store

    Admin->>API: DELETE /admin/documents (document IDs)
    API->>API: Validate request & authenticate admin

    loop For each document ID
        API->>VS: Check if document exists (by ID)
        VS-->>API: Return existing document metadata (if any)

        alt Document exists
            API->>VS: Delete all chunks for document
            VS-->>API: Confirm deletion complete
        else Document not found
            API->>API: Record as not found
        end
    end

    API-->>Admin: 200 OK (deleted count, not found IDs)
```
