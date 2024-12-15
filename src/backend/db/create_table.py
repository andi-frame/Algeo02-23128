from fastapi import HTTPException
from backend.db.index import supabase

def create_tables():
    try:
        supabase.table("playlist").create({
            "id": "uuid DEFAULT uuid_generate_v4() PRIMARY KEY",
            "name": "text NOT NULL",
            "created_at": "timestamp NOT NULL DEFAULT now()"
        }).execute()

        supabase.table("track").create({
            "id": "uuid DEFAULT uuid_generate_v4() PRIMARY KEY",
            "playlist_id": "uuid REFERENCES playlist(id)",
            "name": "text NOT NULL",
            "image_url": "text",
            "music_url": "text",
            "processed_image": "bytea",
            "processed_music": "bytea",
            "created_at": "timestamp NOT NULL DEFAULT now()"
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))