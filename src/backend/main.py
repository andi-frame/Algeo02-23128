import os
import uuid
import tempfile
import json
import zipfile
import traceback
from dotenv import load_dotenv
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI, 
    File, 
    UploadFile, 
    Form, 
    HTTPException,
    Request
)
from fastapi.responses import JSONResponse
from firebase_admin import (
    credentials, 
    initialize_app, 
    storage
)
import firebase_admin

load_dotenv()

FIREBASE_CREDENTIALS_JSON = os.getenv('FIREBASE_CREDENTIALS_JSON')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')

if not FIREBASE_CREDENTIALS_JSON or not FIREBASE_STORAGE_BUCKET:
    raise ValueError("Firebase configuration is missing")

try:
    cred_dict = json.loads(FIREBASE_CREDENTIALS_JSON)
    cred = credentials.Certificate(cred_dict)
except json.JSONDecodeError:
    raise ValueError("Invalid Firebase credentials JSON")

if not firebase_admin._apps:
    firebase_app = initialize_app(cred, {
        'storageBucket': FIREBASE_STORAGE_BUCKET
    })

bucket = storage.bucket()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_zip(
    file: UploadFile = File(...), 
    upload_type: str = Form(...)
):
    """
    Upload ZIP file to Firebase Storage
    
    Args:
    - file: Uploaded ZIP file
    - upload_type: Type of upload (images/audios/mapper)
    
    Returns:
    - Dictionary with upload details
    """
    try:
        valid_types = ['images', 'audios', 'mapper']
        if upload_type not in valid_types:
            raise HTTPException(status_code=400, detail="Invalid upload type")

        unique_filename = f"{upload_type}/{uuid.uuid4()}.zip"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            content = await file.read()
            temp_zip.write(content)
            temp_zip_path = temp_zip.name

        try:
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                if upload_type == 'images':
                    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
                elif upload_type == 'audios':
                    valid_extensions = ('.wav',)
                else: # mapper
                    valid_extensions = ('.txt', '.csv')
                
                invalid_files = [
                    f for f in zip_ref.namelist() 
                    if not f.lower().endswith(valid_extensions)
                ]
                
                if invalid_files:
                    raise ValueError(f"Invalid files in ZIP: {invalid_files}")
        except (zipfile.BadZipFile, ValueError) as zip_error:
            os.unlink(temp_zip_path)
            raise HTTPException(status_code=400, detail=str(zip_error))

        try:
            blob = bucket.blob(unique_filename)
            blob.upload_from_filename(temp_zip_path)
            blob.make_public()
        except:
            pass
    except:
        pass

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("Unexpected error:", traceback.format_exc())
    return JSONResponse(
        status_code=500, 
        content={
            "message": "Internal server error",
            "error": str(exc),
            "traceback": traceback.format_exc()
        }
    )