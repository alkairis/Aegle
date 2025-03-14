import concurrent.futures
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from exception.MedBotException import MedBotException
from util.logger import Logger
from util.constants import HUGGINGFACE_MODEL, HUGGINGFACE_API_KEY

class HFModel:
    def __init__(self, temperature: float):
        self.logger = Logger("HFModel")
        self.temperature=temperature
        self.model_name = HUGGINGFACE_MODEL
        self.llm = self.__load_base_model()

    def __load_base_model(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.__load_base_model_async)
            try:
                return future.result(timeout=120)
            except concurrent.futures.TimeoutError:
                self.logger.error(f"Error: Loading HuggingFace {self.model_name} Model timed out.")
                return None

    def __load_base_model_async(self):
        try:
            self.logger.info(f"Loading HuggingFace {self.model_name} Model.")
            model = HuggingFaceInferenceAPI(
                model_name=self.model_name,
                token=HUGGINGFACE_API_KEY,
                temperature=self.temperature
            )
            self.logger.info(f"HuggingFace {self.model_name} Model loaded successfully.")
            return model
        except MedBotException as e:
            self.logger.error(f"Error: Failed to load HuggingFace {self.model_name} Model. {e}")
            return None