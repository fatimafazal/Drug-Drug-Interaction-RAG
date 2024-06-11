
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import List, Tuple
from pydantic import BaseModel
from operator import itemgetter
from types import SimpleNamespace

import json
import chromadb

#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _make_documents_ids_metadata():
    """
    Create documents, ids, and metadata drug interaction json file.
    
    Returns:
        documents (List): A list of strings representing the content of each document.
        ids (List): A list of strings representing the id of each document.
        metadatas (List): A list of dictionaries representing the metadata of each document.
    """
    with open("prompt.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)[:500]
    documents = [
        f"{item['prompt']}   "
        for item in data
    ]
    ids = [str(i) for i in range(len(documents))]
    metadatas = [{k: v for k, v in item.items() if k != 'prompt' } for item in data]
    
    return documents, ids, metadatas

def _create_or_get_collection():
    """

    Returns:
        collection (chromadb.Collection): A collection object in ChromaDB.
    """
    chroma_client = chromadb.Client()  
    collection = chroma_client.get_or_create_collection(
        name="prompt",
        metadata={"hnsw_space": "cosine"}
    )
    
    return collection

def _query_collection(collection, query_text: str):
    
    #collection = _create_or_get_collection()  # Adjusted to new function
    #print(collection)
    results = collection.query( query_texts=[query_text])
    
    return results

def format_results(results: dict):
    """
    Format the query results from ChromaDB into a list of dictionaries.

    Args:
        results (dict): A dictionary containing the query results.

    Returns:
        formatted_results (list): A list of dictionaries representing the formatted query results.
    """
    distances = results.get('distances', [[]])[0]
    metadatas = results.get('metadatas', [[]])[0]

    if not distances or not metadatas:
        return {}

    top_match_index = distances.index(min(distances))
    top_metadata = metadatas[top_match_index]

    # Return the 'completion' field of the top metadata
    top_result = {
        "id": str(top_match_index), 
        "completion": top_metadata.get('completion')
    }

    return top_result

async def lifespan(app: FastAPI):
    #logging.info("Application startup: Loading data...")
    try:
        documents, ids, metadatas = _make_documents_ids_metadata()
        
        lifespan_namespace.collection = _create_or_get_collection()
        lifespan_namespace.collection.add(documents = documents, ids = ids, metadatas=metadatas)
        app.state.collection = lifespan_namespace.collection
        
        #logging.info("Data successfully loaded.")
    except Exception as e:
        print("Failed to load data: {type(e).__name__} - {e}")
    yield  # If there were cleanup actions, they would go after this yield.




# Define a model for what was previously a SimpleNamespace object
class ResultItem(BaseModel):
    id: str
    score: float
    metadata: dict  # Adjust the type as necessary

class QueryResultsResponse(BaseModel):
    query_text: str
    n_results: int
    results: List[ResultItem]  # Use the defined model here

class QueryResults(BaseModel):
    query_text: str
    n_results: int


lifespan_namespace = SimpleNamespace()
app = FastAPI(lifespan = lifespan)



@app.on_event("startup")
async def startup_event():
    documents, ids, metadatas = _make_documents_ids_metadata()
    collection = _create_or_get_collection()
    try:
        # Assuming `collection.add` is synchronous and returns some indication of success
        add_result = collection.add(documents=documents, ids=ids, metadatas=metadatas)
        #print(f"Documents added to collection: {add_result}")
    except Exception as e:
        print(f"Failed to add documents to collection: {e}")

    # Store the collection in the app state
    app.state.collection = collection


@app.get('/query')
def read_query(query_text: str):
    """
    Query the collection in ChromaDB with the specified query text and number of results.

    Args:
        query_text (str): The query text to search for in the collection.
        n_results (int): The number of results to return.

    Returns:
        result_dict: A dictionary containing the query results.
    """
    #print(app)
    #collection = app.state.collection
    results = _query_collection(lifespan_namespace.collection, query_text)
    
    formatted_results = format_results(results)
    
    
    return formatted_results

from pydantic import BaseModel, constr, Field, validator

class DocumentIDModel(BaseModel):
    """
    Data model for document ID validation.
    Assumes document IDs are alphanumeric strings of a certain length.
    """
    document_id: constr(regex=r'^[a-zA-Z0-9]{8,12}$')
    
    @validator('document_id')
    def id_must_be_alphanumeric(cls, v):
        assert v.isalnum(), 'document_id must be alphanumeric'
        return v

class MetadataModel(BaseModel):
    """
    Data model for document or entity metadata.
    This example assumes metadata includes a title and a description.
    """
    title: constr(max_length=100)
    description: constr(max_length=500)
    
    @validator('title', 'description')
    def fields_must_not_be_empty(cls, v, field):
        if not v.strip():
            raise ValueError(f'{field.name} must not be empty')
        return v
 
from pydantic import BaseModel, PositiveInt, constr
from datetime import date

class DocumentID(BaseModel):
    id: str # Assuming document IDs are positive integers

class Metadata(BaseModel):
    Metadata: str
    
    
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fetch_document_details(doc_id: str):
    collection = lifespan_namespace.collection
    query_text = f"id:{doc_id}"  
    results = collection.query(query_texts=[query_text])
    return format_results(results)

#def fetch_document_details(doc_id: str, db:Session):
 #   return db.query(documents).filter(documents.id == doc_id).first()

def update_metadata(doc_id: str, metadata: str, db: Session):
    db.query(documents).filter(documents.id == doc_id).update(metadata)
    db.commit()
    return True


from sqlalchemy.orm import Session
from fastapi import HTTPException

@app.post("/document/details")
def get_document_details(document_id: DocumentID):
    document_details = fetch_document_details(document_id.id, get_db())
    print(document_details)
    if document_details is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document_details


@app.post("/document/update_metadata")
def update_document_metadata(document_id: int, metadata: Metadata):
    if not update_metadata(document_id, metadata.dict()):
        raise HTTPException(status_code=500, detail="Failed to update metadata")
    return {"message": "Metadata updated successfully."}
