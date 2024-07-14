import os
import boto3
from azure.storage.blob import BlobServiceClient
from config import Config
from docx import Document
from .rag_utils import initialize_rag
import logging
import os
from typing import List, Dict, Optional
from .rag_utils import initialize_rag
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_grounding_data() -> List[Dict[str, str]]:
    if not Config.USE_GROUNDING:
        logger.info("Grounding is disabled")
        return []

    logger.info(f"Loading grounding data from source: {Config.GROUNDING_SOURCE}")
    grounding_data = []
    if Config.GROUNDING_SOURCE == "local":
        grounding_data = load_local_grounding_data()
    elif Config.GROUNDING_SOURCE == "s3":
        grounding_data = load_s3_grounding_data()
    elif Config.GROUNDING_SOURCE == "azure":
        grounding_data = load_azure_grounding_data()
    else:
        logger.error(f"Unknown grounding source: {Config.GROUNDING_SOURCE}")
    
    logger.info(f"Loaded {len(grounding_data)} grounding documents")
    
    if grounding_data:
        logger.info("Initializing RAG system with grounding data")
        initialize_rag(grounding_data)
    else:
        logger.warning("No grounding data found. RAG system will not be initialized.")
    
    return grounding_data

def load_local_grounding_data() -> List[Dict[str, str]]:
    grounding_data = []
    for filename in os.listdir(Config.GROUNDING_PATH):
        file_path = os.path.join(Config.GROUNDING_PATH, filename)
        if os.path.isfile(file_path):
            content = read_file_with_fallback_encoding(file_path)
            if content is not None:
                grounding_data.append({"filename": filename, "content": content})
    return grounding_data

def read_file_with_fallback_encoding(file_path: str) -> Optional[str]:
    encodings = ['utf-8', 'latin-1', 'ascii']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            logger.warning(f"Failed to decode {file_path} with {encoding} encoding. Trying next encoding.")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return None
    
    logger.error(f"Failed to read {file_path} with all attempted encodings.")
    return None


__all__ = ['load_grounding_data']

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def load_s3_grounding_data():
    s3 = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )
    grounding_data = []
    
    response = s3.list_objects_v2(Bucket=Config.AWS_BUCKET_NAME)
    for obj in response.get('Contents', []):
        if obj['Key'].endswith(('.txt', '.docx')):
            file_content = s3.get_object(Bucket=Config.AWS_BUCKET_NAME, Key=obj['Key'])['Body'].read()
            if obj['Key'].endswith('.txt'):
                content = file_content.decode('utf-8')
            elif obj['Key'].endswith('.docx'):
                with open('temp.docx', 'wb') as temp_file:
                    temp_file.write(file_content)
                content = read_docx('temp.docx')
                os.remove('temp.docx')
            grounding_data.append({"filename": obj['Key'], "content": content})
    
    return grounding_data

def load_azure_grounding_data():
    blob_service_client = BlobServiceClient.from_connection_string(Config.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(Config.AZURE_CONTAINER_NAME)
    
    grounding_data = []
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        if blob.name.endswith(('.txt', '.docx')):
            blob_client = container_client.get_blob_client(blob.name)
            file_content = blob_client.download_blob().readall()
            if blob.name.endswith('.txt'):
                content = file_content.decode('utf-8')
            elif blob.name.endswith('.docx'):
                with open('temp.docx', 'wb') as temp_file:
                    temp_file.write(file_content)
                content = read_docx('temp.docx')
                os.remove('temp.docx')
            grounding_data.append({"filename": blob.name, "content": content})
    
    return grounding_data

__all__ = ['load_grounding_data']