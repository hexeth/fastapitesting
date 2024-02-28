from typing import List
import aiohttp
import time
from fastapi import FastAPI, HTTPException, UploadFile
from azure.storage.blob.aio import BlobServiceClient

app = FastAPI()

@app.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile]):
    start_time = time.time()
    results = []
    for file in files:
        name = file.filename
        type = file.content_type
        result = await uploadtoazure(file, name, type)
        results.append(result)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total script time    taken: {elapsed_time} seconds")
    return results


async def uploadtoazure(file: UploadFile,file_name: str,file_type:str):
    start_time = time.time()
    connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "testcontainer"
    async with blob_service_client:
            container_client = blob_service_client.get_container_client(container_name)
            try:
                blob_client = container_client.get_blob_client(file_name)
                f = await file.read()
                await blob_client.upload_blob(f)
            except Exception as e:
                print(e)
                raise e
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time} seconds")
    return "{'did_it_work':'yeah it did!'}"