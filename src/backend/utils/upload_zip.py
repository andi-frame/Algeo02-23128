from fastapi import HTTPException
from backend.db.index import supabase

async def process_zip_metadata(upload_type, zip_file_name):
    """
    Process and save metadata related to the uploaded ZIP file.
    
    Args:
    - upload_type: Type of upload (images, audios, mapper)
    - zip_file_name: Name of the uploaded ZIP file
    
    Returns:
    - Metadata details that were saved
    """
    try:
        response = supabase.table('file_metadata').insert({
            'upload_type': upload_type,
            'file_name': zip_file_name,
            'status': 'uploaded'
        }).execute()

        if response.error:
            raise Exception("Error saving metadata to database")

        return response.data

    except Exception as e:
        print(f"Error processing metadata: {e}")
        raise HTTPException(status_code=500, detail=str(e))