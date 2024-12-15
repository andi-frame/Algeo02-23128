from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from backend.services.upload_service import upload_zip

upload_router = APIRouter()

@upload_router.post("/upload")
async def upload(file: UploadFile = File(...), upload_type: str = Form(...)):
    """
    Endpoint to handle file upload
    """
    try:
        response = await upload_zip(file, upload_type)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
