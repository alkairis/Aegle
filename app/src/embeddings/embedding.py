from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import concurrent.futures
from llama_index.core import Settings, load_index_from_storage, StorageContext
from exception.MedBotException import MedBotException
from util.logger import Logger
from src.embeddings.model import HFModel
from util.constants import HUGGINGFACE_EMBED_MODEL, HUGGINGFACE_API_KEY


class Embedding:
    def __init__(self, llm: HFModel):
        self.logger = Logger("EmbeddingModel")
        self.embed_model = self.__load_embedding_model()
        self.llm = llm
        self.index=self.set_settings()

    def __load_embedding_model(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.__load_embedding_model_async)
            try:
                return future.result(timeout=120)
            except concurrent.futures.TimeoutError:
                self.logger.error("Error: Loading Embedding Model timed out.")
                return None

    def __load_embedding_model_async(self):
        try:
            self.logger.info("Loading HuggingFace Embedding Model.")
            embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en")
            self.logger.info("HuggingFace Embedding Model loaded successfully.")
            return embed_model
        except MedBotException as e:
            self.logger.error(f"Error: Failed to load Embedding Model. {e}")
            return None

    def set_settings(self):
        Settings.embed_model = self.embed_model
        Settings.llm = self.llm
        self.logger.info("Set Settings!")
