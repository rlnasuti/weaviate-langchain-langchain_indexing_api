Hail and well met!

## What is this?

Demonstration of how to piece together various pieces of functionality using Langchain and Weaviate

Some things in here:
- docker compose file used to setup an instance of Weaviate locally that will work with the langchain indexing api.
- indexing_api: demonstrates how to populate the weaviate database (note: if you look at the objects you'll notice that there's a vector_weights property that's empty. This is fine - vector similarity search still works. IDK what's happening but the embeddings must be somewhere else.)
- client.py: demonstrates how to use self-querying retriever as well as do a standard similarity search filtering on metadata.
