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
import numpy as np
from backend.functions.Album_Finder import data_centering, singular_value_decomposition, query_projection, compute_euclidean_distance
from backend.functions.audio import process

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
    playlistImage: UploadFile = File(...),
    audios: UploadFile = File(...),
    mapper: UploadFile = File(...)
):
    try:
        datetimenow = datetime.now().isoformat()

        images_zip = zipfile.ZipFile(BytesIO(await images.read()))
        audios_zip = zipfile.ZipFile(BytesIO(await audios.read()))
        playlistImages_content = await playlistImage.read()
        mapper_content = await mapper.read()
        mapper_data = json.loads(mapper_content.decode('utf-8'))

        # Upload playlist image
        playlist_img_path = f"HMO/{playlistName}_{datetimenow}/playlist/{datetime.now().isoformat()}.png"
        playlist_img_url = upload_to_firebase(playlist_img_path, playlistImages_content, "image/png")
        
        playlist_id = str(uuid.uuid4())
        supabase.table('playlist').insert({
            'id': playlist_id,
            'name': playlistName,
            'created_at': datetimenow,
            'img_url' : playlist_img_url
        }).execute()

        image_paths = [images_zip.open(item['pic_name']) for item in mapper_data]
        myu, standardized_data = data_centering(image_paths)
        projections, Uk, _ = singular_value_decomposition(standardized_data, 2)

        supabase.table('playlist').update({
            'myu': myu.tolist(),
            'uk': Uk.tolist(),
            'projections': projections.tolist()
        }).eq('id', playlist_id).execute()

        
        for idx, item in enumerate(mapper_data):
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
            audio_path = f"HMO/{playlistName}_{datetimenow}/audios/{name}_{datetime.now().isoformat()}.mid"
            print(f"Uploading {audio_path}...\n")
            audio_url = upload_to_firebase(audio_path, audio_content, "audio/midi")

            # Extract audio file for processing
            audio_blob = BytesIO(audio_content)
            audio_vector = process(audio_blob)

            # Insert track into the database
            supabase.table('track').insert({
                'playlist_id': playlist_id,
                'name': name,
                'image_url': image_url,
                'music_url': audio_url,
                'image_idx': idx,
                'processed_music': audio_vector,
            }).execute()

        return JSONResponse(content={"message": "Files uploaded successfully"})
    
    except Exception as e:
        print("Error during file upload:", e)
        logging.error("Error during file upload: %s", e, exc_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/get-all-playlist")
async def get_all_playlist():
    try:
        playlists = supabase.table("playlist").select("id, name, img_url").execute()
        if not playlists.data:
            raise HTTPException(status_code=404, detail="No playlists found")

        return JSONResponse(content={"playlists": playlists.data})

    except Exception as e:
        print(f"Error getting playlists: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/get-tracks-by-playlistId")
async def get_tracks_by_playlistId(playlistId: str):
    try:
        # Query the tracks based on the playlist ID
        tracks = supabase.table("track").select("id, name, image_url, music_url").eq("playlist_id", playlistId).execute()

        if not tracks.data:
            raise HTTPException(status_code=404, detail="No tracks found for this playlist")

        return JSONResponse(content={"tracks": tracks.data})

    except Exception as e:
        print(f"Error fetching tracks for playlist {playlistId}: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/query-by-image")
async def query_by_image(
    query_image: UploadFile = File(...), 
    top_k: int = Form(...) 
):
    try:
        query_image_content = await query_image.read()
        query_image_blob = BytesIO(query_image_content)
        
        svd_data_records = supabase.table('playlist').select('id, myu, uk, projections, name, track(id, image_url, music_url, name)').execute()
        svd_data = svd_data_records.data

        all_similarities = []

        for record in svd_data:
            myu = np.array(record['myu'])
            Uk = np.array(record['uk'])
            projections = np.array(record['projections'])
            playlist_id = record['id']
            playlist_name = record['name']
            tracks = record['track']

            query_proj = query_projection(query_image_blob, myu, Uk)

            distances = compute_euclidean_distance(query_proj, projections)
            max_distance = max(distances)

            for idx, distance in enumerate(distances):
                similarity_percentage = (1 - (distance / max_distance)) * 100 

                all_similarities.append({
                    'distance': distance,
                    'similarity_percentage': round(similarity_percentage, 2),
                    'playlist_id': playlist_id,
                    'playlist_name': playlist_name,
                    'track_idx': idx,
                    'image_url': tracks[idx]['image_url'],
                    'music_url': tracks[idx]['music_url'],
                    'track_name': tracks[idx]['name']
                })

        all_similarities = sorted(all_similarities, key=lambda x: x['distance'])
        top_tracks = all_similarities[:top_k]

        return JSONResponse(content={"top_tracks": top_tracks})
    except Exception as e:
        print("Error during query:", e)
        logging.error("Error during query: %s", e, exc_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)