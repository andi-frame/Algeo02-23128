from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import zipfile
from io import BytesIO
import json
from datetime import datetime
from backend.db.index import supabase
from backend.db.index import bucket
import uuid
import logging

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

def upload_to_firebase(file_path, file_content, mimetype):
    blob = bucket.blob(file_path)
    blob.upload_from_string(file_content, content_type=mimetype)
    blob.make_public()
    return blob.public_url


@app.post("/upload")
async def upload_files(
    playlistName: str = Form(...),
    images: UploadFile = File(...),
    audios: UploadFile = File(...),
    mapper: UploadFile = File(...)
):
    try:
        datetimenow = datetime.now().isoformat()

        # Extract and process the uploaded files
        images_zip = zipfile.ZipFile(BytesIO(await images.read()))
        audios_zip = zipfile.ZipFile(BytesIO(await audios.read()))
        mapper_content = await mapper.read()
        
        # Ensure mapper.json is in the expected format
        mapper_data = json.loads(mapper_content.decode('utf-8'))

        # Create a new playlist entry
        playlist_id = str(uuid.uuid4())
        supabase.table('playlist').insert({
            'id': playlist_id,
            'name': playlistName,
            'created_at': datetimenow
        }).execute()
        
        for item in mapper_data:
            name = item['audio_name']
            image_filename = item['pic_name']
            audio_filename = item['audio_file']
            
            # Extract and upload image
            image_file = images_zip.open(image_filename)
            image_content = image_file.read()
            image_path = f"HMO/{playlistName}_{datetimenow}/images/{name}_{datetime.now().isoformat()}.png"
            print(f"Uploading {image_path}...\n")
            image_url = upload_to_firebase(image_path, image_content, "image/png")

            # Extract and upload audio
            audio_file = audios_zip.open(audio_filename)
            audio_content = audio_file.read()
            audio_path = f"HMO/{playlistName}_{datetimenow}/audios/{name}_{datetime.now().isoformat()}.wav"
            print(f"Uploading {audio_path}...\n")
            audio_url = upload_to_firebase(audio_path, audio_content, "audio/wav")

            # Insert track into the database
            supabase.table('track').insert({
                'playlist_id': playlist_id,
                'name': name,
                'image_url': image_url,
                'music_url': audio_url,
            }).execute()

        return JSONResponse(content={"message": "Files uploaded successfully"})
    
    except Exception as e:
        print("Error during file upload:", e)
        logging.error("Error during file upload: %s", e, exc_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)