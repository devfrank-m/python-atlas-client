# Atlas Client

The Python client for the [Atlas](https://github.com/devfrank-m/atlas) vector database.

## Installation

```bash
pip install atlas-db-client
```

## Quick Start

```python
from atlas import AtlasClient

client = AtlasClient(host="http://localhost:8600")

# Create a collection
collection = client.create_collection(
    name="my-collection",
    dimension=128,
    metric="cosine",
)

# Insert a vector
result = client.insert_vector(
    collection_id=collection.id,
    vector=[0.1] * 128,
    metadata={"label": "example"},
)

# Search
response = client.search(
    collection_id=collection.id,
    vector=[0.1] * 128,
    k=5,
)

for r in response.results:
    print(r.id, r.score)
```

## Async Support

```python
from atlas import AsyncAtlasClient

async with AsyncAtlasClient() as client:
    collection = await client.create_collection(
        name="my-collection",
        dimension=128,
        metric="cosine",
    )
```

## License

MIT
