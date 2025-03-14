from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from util.constants import PINECONE_API_KEY, PINECONE_INDEX

from util.logger import Logger


class PineconeClient:
    def __init__(self):
        self.logger = Logger("pinecone")
        self.__pc = Pinecone(api_key=PINECONE_API_KEY)
        
        self.logger.info(f"Checking pinecone index : {PINECONE_INDEX}")
        if not self.__pc.has_index(PINECONE_INDEX):
            self.logger.info(f"Creating pinecone index : {PINECONE_INDEX}")
            self.__pc.create_index(
                PINECONE_INDEX,
                dimension=1024,
                metric="cosine",
                spec = ServerlessSpec(cloud="aws", region="us-east-1")
            )
            self.logger.info(f"Pinecone index created successfully. {PINECONE_INDEX}")

    def get_vector_store(self):
        pinecone_index = self.__pc.Index(PINECONE_INDEX)
        self.logger.info(f"Pinecone index *{PINECONE_INDEX}* loaded successfully. ")
        return PineconeVectorStore(pinecone_index=pinecone_index)
