import os
import uuid
import tempfile
import zipfile
from fastapi import HTTPException
from backend.db.index import bucket
from backend.utils.upload_zip import process_zip_metadata  # Import utility function for metadata

async def upload_zip(file, upload_type):
    """
    Upload a ZIP file to Firebase Storage and process metadata.
    
    Args:
    - file: Uploaded file (Zip)
    - upload_type: Type of upload (images, audios, mapper)
    
    Returns:
    - Response indicating the upload was successful
    """
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
            else:
                valid_extensions = ('.txt', '.csv')

            invalid_files = [
                f for f in zip_ref.namelist() if not f.lower().endswith(valid_extensions)
            ]

            if invalid_files:
                raise ValueError(f"Invalid files in ZIP: {invalid_files}")
    except (zipfile.BadZipFile, ValueError) as zip_error:
        os.unlink(temp_zip_path)
        raise HTTPException(status_code=400, detail=str(zip_error))

    try:
        # Upload the ZIP file to Firebase
        blob = bucket.blob(unique_filename)
        blob.upload_from_filename(temp_zip_path)
        blob.make_public()
    except Exception as e:
        os.unlink(temp_zip_path)
        raise HTTPException(status_code=500, detail=f"Error uploading to Firebase: {str(e)}")

    # Process and save metadata to Supabase
    await process_zip_metadata(upload_type, unique_filename)

    # Clean up the temporary file
    os.unlink(temp_zip_path)

    return {"message": "Upload successful", "filename": unique_filename}
