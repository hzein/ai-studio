import os

# from dotenv import load_dotenv
from chromadb.config import Settings

# https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/excel.html?highlight=xlsx#microsoft-excel
from langchain_community.document_loaders import (
    CSVLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredExcelLoader,
    Docx2txtLoader,
)

# from langchain_community.document_loaders import (
#     UnstructuredFileLoader,
#     UnstructuredMarkdownLoader,
# )
from langchain_community.document_loaders import UnstructuredHTMLLoader


# load_dotenv()
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

print(f"ROOT_DIRECTORY: {ROOT_DIRECTORY}")

# Define the folder for storing database
SOURCE_DIRECTORY = f"{ROOT_DIRECTORY}/source_documents"

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/db"

FILE_INGEST_File = f"{ROOT_DIRECTORY}/file_ingest.log"

RESPONSE_OUTPUT_FILE = f"{ROOT_DIRECTORY}/response_output.csv"

MODELS_PATH = f"{ROOT_DIRECTORY}/models"

SAVE_QA = True
SHOW_SOURCES = True
USE_HISTORY = True

# Crypt secret and algorithm for hashing
SECRET_KEY = "2b9627584fef2000e5b48b886858bff1e3f26d817249e2c5167fa2643d305a5c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30

# Can be changed to a specific number
INGEST_THREADS = os.cpu_count() or 8

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    anonymized_telemetry=False,
    is_persistent=True,
)

# Context Window and Max New Tokens
CONTEXT_WINDOW_SIZE = 4096
MAX_NEW_TOKENS = CONTEXT_WINDOW_SIZE  # int(CONTEXT_WINDOW_SIZE/4)

#### If you get a "not enough space in the buffer" error, you should reduce the values below, start with half of the original values and keep halving the value until the error stops appearing

N_GPU_LAYERS = 20  # Llama-2-70B has 83 layers
N_BATCH = 512

### From experimenting with the Llama-2-7B-Chat-GGML model on 8GB VRAM, these values work:
# N_GPU_LAYERS = 20
# N_BATCH = 512


# https://python.langchain.com/en/latest/_modules/langchain/document_loaders/excel.html#UnstructuredExcelLoader
DOCUMENT_MAP = {
    ".html": UnstructuredHTMLLoader,
    ".txt": TextLoader,
    # ".md": UnstructuredMarkdownLoader,
    ".py": TextLoader,
    # ".pdf": PDFMinerLoader,
    ".pdf": "UnstructuredFileLoader",
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}

# Default Instructor Model
# EMBEDDING_MODEL_NAME = "hkunlp/instructor-large"  # Uses 1.5 GB of VRAM (High Accuracy with lower VRAM usage)
# EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

####
#### OTHER EMBEDDING MODEL OPTIONS
####

# EMBEDDING_MODEL_NAME = "hkunlp/instructor-xl" # Uses 5 GB of VRAM (Most Accurate of all models)
# EMBEDDING_MODEL_NAME = "intfloat/e5-large-v2" # Uses 1.5 GB of VRAM (A little less accurate than instructor-large)
# EMBEDDING_MODEL_NAME = "intfloat/e5-base-v2" # Uses 0.5 GB of VRAM (A good model for lower VRAM GPUs)
# EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # Uses 0.2 GB of VRAM (Less accurate but fastest - only requires 150mb of vram)


#### SELECT AN OPEN SOURCE LLM (LARGE LANGUAGE MODEL)
# Select the Model ID and model_basename
# load the LLM for generating Natural Language responses

#### GPU VRAM Memory required for LLM Models (ONLY) by Billion Parameter value (B Model)
#### Does not include VRAM used by Embedding Models - which use an additional 2GB-7GB of VRAM depending on the model.
####
#### (B Model)   (float32)    (float16)    (GPTQ 8bit)         (GPTQ 4bit)
####    7b         28 GB        14 GB       7 GB - 9 GB        3.5 GB - 5 GB
####    13b        52 GB        26 GB       13 GB - 15 GB      6.5 GB - 8 GB
####    32b        130 GB       65 GB       32.5 GB - 35 GB    16.25 GB - 19 GB
####    65b        260.8 GB     130.4 GB    65.2 GB - 67 GB    32.6 GB -  - 35 GB

####
#### (FOR GGUF MODELS)
####

# MODEL_ID = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
# MODEL_BASENAME = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"


####
#### (FOR GPTQ QUANTIZED)
####


# MODEL_ID = "TheBloke/zephyr-7B-beta-GPTQ"
# MODEL_BASENAME = "zephyr-7B-beta-GPTQ"

# MODEL_ID = "TheBloke/zephyr-7B-beta-GPTQ"
# MODEL_BASENAME = "zephyr-7B-beta-GPTQ-4bit-32g-actorder_True"

MODEL_ID = "TheBloke/CapybaraHermes-2.5-Mistral-7B-GPTQ"
MODEL_BASENAME = "CapybaraHermes-2.5-Mistral-7B-GPTQ"

####
#### (FOR GGML) (Quantized cpu+gpu+mps)
####


####
#### (FOR AWQ QUANTIZED)
####
