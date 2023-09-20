from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import os
from dotenv import load_dotenv
import weaviate

load_dotenv()

metadata_field_info = [
    AttributeInfo(
        name="genre",
        description="The genre of the movie",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="year",
        description="The year the movie was released",
        type="integer",
    ),
    AttributeInfo(
        name="director",
        description="The name of the movie director",
        type="string",
    ),
    AttributeInfo(
        name="rating", description="A 1-10 rating for the movie", type="float"
    ),
]

embeddings = OpenAIEmbeddings()
collection_name = "Test_index"


# create the vector store - url defined in .env
client = weaviate.Client(url=os.getenv("WEAVIATE_URL"))

vectorstore = Weaviate(
    client = client,
    index_name=collection_name, 
    text_key="page_content",
    embedding=embeddings,
    attributes=["source", "director", "year", "rating", "genre"]
)

document_content_description = "Brief summary of a movie"
llm = OpenAI(temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm, vectorstore, document_content_description, metadata_field_info, verbose=True
)

# This example specifies a query and a filter
# retrievals = retriever.get_relevant_documents("Has Greta Gerwig directed any movies about fish")
where_filter = {"path": ["director"], "operator": "Equal", "valueString": "Greta Gerwig"}
retrievals = vectorstore.similarity_search(query="dinosaurs", k=1, where_filter=where_filter)
print(retrievals)