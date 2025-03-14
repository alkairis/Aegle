from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

from src.embeddings.pinecone_client import PineconeClient
from src.MedicalBot import MedicalBot

app = FastAPI()

bot = MedicalBot()

class QueryRequest(BaseModel):
    query: str

def embed_documents_task():
    """Function to load and embed documents in the background."""
    try:
        pc = PineconeClient()
        documents = bot.load_documents()
        bot.pinecone_vector_index = bot.init_pinecone_vector_store_index(documents, pc.get_vector_store())
        bot.logger.info("Documents successfully embedded in Pinecone.")
    except Exception as e:
        bot.logger.error(f"Error in embedding documents: {str(e)}")
        
@app.post("/ask")
async def ask_question(request: QueryRequest):
    """Handles user queries using the MedicalBot's execute_query method."""
    try:
        response = bot.execute_query(request.query)
        return {"answer": response.response if hasattr(response, 'response') else response}
    except Exception as e:
        bot.logger.error(f"Error in /ask: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process query")


@app.post("/embed")
async def embed_documents(background_tasks: BackgroundTasks):
    """Triggers the embedding process in the background."""
    background_tasks.add_task(embed_documents_task)
    return {"message": "Embedding process started in the background"}