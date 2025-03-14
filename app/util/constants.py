import os
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

def __get_env(key: str) -> Optional[str]:
    """
    Retrieve the value of an environment variable.

    Args:
        key (str): The name of the environment variable to retrieve.

    Returns:
        Optional[str]: The value of the environment variable if it exists, 
        otherwise None.
    """
    return os.getenv(key)

PINECONE_API_KEY = __get_env("PINECONE_API_KEY")
HUGGINGFACE_API_KEY = __get_env("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = __get_env("HUGGINGFACE_MODEL")
PINECONE_INDEX=__get_env("PINECONE_INDEX")
HUGGINGFACE_EMBED_MODEL=__get_env("HUGGINGFACE_EMBED_MODEL")
PROJECT_DIR = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..'))
VECTOR_DB_PATH = "vector_storage/"
