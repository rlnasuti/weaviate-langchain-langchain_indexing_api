from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import SQLRecordManager, index
from langchain.schema import Document
from langchain.vectorstores import Weaviate
import os
from dotenv import load_dotenv
import weaviate

load_dotenv()

embeddings = OpenAIEmbeddings()

collection_name = "test_index"

def _clear():
    """Hacky helper method to clear content. See the `full` mode section to to understand why it works."""
    index([], record_manager, vectorstore, cleanup="full", source_id_key="source")

embedding = OpenAIEmbeddings()

# create the vector store - url defined in .env
client = weaviate.Client(url=os.getenv("WEAVIATE_URL"))

vectorstore = Weaviate(
    client = client,
    index_name=collection_name, 
    text_key="page_content",
    embedding=embeddings
)

namespace = f"weaviate/{collection_name}"
record_manager = SQLRecordManager(
    namespace, db_url="sqlite:///record_manager_cache.sql"
)
record_manager.create_schema()

docs = [
    Document(
        page_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",
        metadata={"source": "hard coded", "year": 1993, "rating": 7.7, "genre": "science fiction"},
    ),
    Document(
        page_content="Leo DiCaprio gets lost in a dream within a dream within a dream within a ...",
        metadata={"source": "hard coded", "year": 2010, "director": "Christopher Nolan", "rating": 8.2},
    ),
    Document(
        page_content="A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea",
        metadata={"source": "hard coded", "year": 2006, "director": "Satoshi Kon", "rating": 8.6},
    ),
    Document(
        page_content="A bunch of normal-sized women are supremely wholesome and some men pine after them",
        metadata={"source": "hard coded", "year": 2019, "director": "Greta Gerwig", "rating": 8.3},
    ),
    Document(
        page_content="Toys come alive and have a blast doing so",
        metadata={"source": "hard coded", "year": 1995, "genre": "animated"},
    ),
    Document(
        page_content="Three men walk into the Zone, three men walk out of the Zone",
        metadata={
            "source": "hard coded",
            "year": 1979,
            "rating": 9.9,
            "director": "Andrei Tarkovsky",
            "genre": "science fiction",
        },
    ),
]

res = index(
    docs,
    record_manager,
    vectorstore,
    cleanup=None,
    source_id_key="source",
)

print(res)