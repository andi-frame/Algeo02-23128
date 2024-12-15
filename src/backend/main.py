from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import zipfile
from io import BytesIO
import json
import os
import datetime
from backend.db.index import supabase
from backend.db.index import bucket

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_files(
    playlistName: str = "Playlist Name",
    images: UploadFile = File(...),
    audios: UploadFile = File(...),
    mapper: UploadFile = File(...)
):
    try:
        # Extract and process the uploaded files
        images_zip = zipfile.ZipFile(BytesIO(await images.read()))
        audios_zip = zipfile.ZipFile(BytesIO(await audios.read()))
        mapper_content = await mapper.read()
        
        # Ensure mapper.json is in the expected format
        mapper_data = mapper_content.decode('utf-8')
        mapper_list = json.loads(mapper_data)
        
        # Debug: Print mapper_list to confirm format
        print("Mapper List:", mapper_list)
        
        # Process images and audios
        for file_info in images_zip.infolist():
            print(f"Extracting image: {file_info.filename}")
            with images_zip.open(file_info) as file:
                # Process each image (e.g., upload to Firebase)
                pass

        for file_info in audios_zip.infolist():
            print(f"Extracting audio: {file_info.filename}")
            with audios_zip.open(file_info) as file:
                # Process each audio (e.g., upload to Firebase)
                pass
        
        return JSONResponse(content={"message": "Files uploaded successfully"})
    
    except Exception as e:
        print("Error during file upload:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)