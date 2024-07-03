import os
import boto3
from azure.storage.blob import BlobServiceClient
from config import Config
from docx import Document

def load_grounding_data():
    if not Config.USE_GROUNDING:
        return []

    if Config.GROUNDING_SOURCE == "local":
        return load_local_grounding_data()
    elif Config.GROUNDING_SOURCE == "s3":
        return load_s3_grounding_data()
    elif Config.GROUNDING_SOURCE == "azure":
        return load_azure_grounding_data()
    else:
        print(f"Unknown grounding source: {Config.GROUNDING_SOURCE}")
        return []

def load_local_grounding_data():
    grounding_data = []
    for filename in os.listdir(Config.GROUNDING_PATH):
        file_path = os.path.join(Config.GROUNDING_PATH, filename)
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding='utf-8') as f:
                content = f.read()
                grounding_data.append({"filename": filename, "content": content})
        elif filename.endswith(".docx"):
            content = read_docx(file_path)
            grounding_data.append({"filename": filename, "content": content})
    return grounding_data

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