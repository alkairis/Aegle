import os
from exception.MedBotException import MedBotException
from util.logger import Logger
from src.embeddings.embedding import Embedding
from src.embeddings.model import HFModel
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import StorageContext, SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.chat_engine.types import ChatMode
from src.embeddings.pinecone_client import PineconeClient
from src.prompt.Prompt import Prompt, get_context_prompt
from util.constants import PROJECT_DIR
from llama_index.core.ingestion import IngestionPipeline


class MedicalBot:
    def __init__(self):
        self.logger = Logger("MedicalBot")
        self.pc = PineconeClient()
        self.llm = HFModel(0.02).llm
        self.embedding_llm = Embedding(llm=self.llm)
        self.prompt=Prompt()
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=15000)
        self.pinecone_vector_index=None
        self.reload_vector_store()
        

    def reload_vector_store(self):
        self.logger.info("Loading and embedding documents...")
        # documents = self.load_documents()
        documents = ""
        self.pinecone_vector_index = self.init_pinecone_vector_store_index(documents, self.pc.get_vector_store())
        self.logger.info("Vector store index loaded")

    def execute_query(self, query):
        self.logger.info(f"Query received: {query}")
        
        if not self.pinecone_vector_index:
            self.logger.error("Vector index is not initialized. Run /embed first.")
            return {"error": "Vector index not initialized. Please embed documents first."}

        chat_engine = self.pinecone_vector_index.as_chat_engine(
            chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
            memory=self.memory,
            llm=self.llm,
            text_qa_template=self.prompt.get_text_qa_template(),
            refine_template=self.prompt.get_refine_template(),
            context_prompt=get_context_prompt(),
            verbose=True
        )
        
        self.logger.info("Calling LLM Engine with Query and rag details")
        data = chat_engine.chat(query)
        if data:
            self.logger.info(f"Response received from the query engine {data.response}")
            self.logger.info(data)
            return {"answer": data.response}
        else:
            return {'answer': 'Failed to get query response'}

    def load_documents(self):
        self.logger.info(f"Reading first 20 pages of documents from local storage")   
        reader = SimpleDirectoryReader(input_dir=os.path.join(PROJECT_DIR, "resources/"))
        documents = reader.load_data()
        for i in documents:
            self.logger.debug(f"Document {i.metadata.get('file_name', 'Unknown')} loaded")
        return documents


    def init_pinecone_vector_store_index(self, chunked_document, vector_store=PineconeVectorStore):
        self.logger.info("Initializing Pinecone Vector Store Index...")
        
        if not isinstance(vector_store, PineconeVectorStore):
            raise ValueError("Invalid Vector Store instance. Expected PineconeVectorStore instance.")
        
        # self.logger.info("Applying transformation on documents...")
        # pipeline = IngestionPipeline(
        #     transformations=[
        #         SentenceSplitter(chunk_size=1024, chunk_overlap=20),
        #         self.embedding_llm.embed_model
        #     ],
        #     vector_store=vector_store
        # )
        # self.logger.info("Running pinecone ingestion pipeline...")
        # pipeline.run(documents=chunked_document)
        self.logger.info("Vector store index loaded")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        return index